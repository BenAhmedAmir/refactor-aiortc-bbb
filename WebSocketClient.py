import ast
import asyncio
import json
import websockets
from aiortc import RTCPeerConnection, RTCConfiguration, RTCSessionDescription, RTCIceCandidate, RTCIceServer, \
    RTCRtpCodecParameters, RTCRtpCapabilities, RTCRtpSender
from aiortc.rtcrtpparameters import RTCRtcpFeedback, RTCRtpCodecCapability

from Logger import configure_logger
from ScreenCaptureTrack import ScreenShareTrack

logger = configure_logger()


def modify_sdp(sdp):
    sdp_lines = sdp.split('\r\n')

    # Insert additional attributes or modify existing ones
    sdp_lines = [line if not line.startswith('a=msid-semantic:') else 'a=msid-semantic: WMS *' for line in
                 sdp_lines]

    # Add extmap-allow-mixed attribute
    session_attributes = ['a=extmap-allow-mixed']
    sdp_lines[4:4] = session_attributes  # Assuming session attributes start at line 4

    # Add additional codec mappings and attributes for video
    video_attributes = [
        'a=rtpmap:97 VP8/90000',
        'a=rtpmap:102 H264/90000',
        'a=rtcp-fb:102 goog-remb',
        'a=rtcp-fb:102 transport-cc',
        'a=rtcp-fb:102 ccm fir',
        'a=rtcp-fb:102 nack',
        'a=rtcp-fb:102 nack pli',
        'a=fmtp:102 level-asymmetry-allowed=1;packetization-mode=1;profile-level-id=42001f'
    ]
    for i, line in enumerate(sdp_lines):
        if line.startswith('m=video'):
            sdp_lines[i:i] = video_attributes
            break

    # Join modified SDP lines
    return '\r\n'.join(sdp_lines)


class WebSocketClient:
    def __init__(self, **kwargs):
        self.screen_sharing = None
        self.screen_share_track = None
        self.screen_share_sender = None
        self.id = kwargs.get("id", "start")
        self.type = kwargs.get("sfu_component", "screenshare")
        self.contentType = kwargs.get("sfu_component", "screenshare")
        self.internalMeetingId = kwargs.get("internalMeetingId")
        self.voiceBridge = kwargs.get("voiceBridge")
        self.userName = kwargs.get("userName")
        self.callerName = kwargs.get("callerName")
        self.hasAudio = kwargs.get("hasAudio", False)
        self.bitrate = kwargs.get("bitrate", 1500)
        self.cookies = kwargs.get("cookies")
        self.turn_servers = kwargs.get("turn_servers", [])
        self.ws_url = kwargs.get("ws_url")
        self.role = kwargs.get("role", "viewer")  # Ensure role is provided
        self.pc = RTCPeerConnection(RTCConfiguration(iceServers=self._parse_turn_servers()))
        self.websocket = None

    async def connect(self):
        """Establish a connection to the WebSocket server."""
        try:
            self.websocket = await websockets.connect(self.ws_url, extra_headers={"Cookie": self.cookies})
            logger.info(f"Connected to WebSocket server at {self.ws_url}")

            # Setup event handlers for ICE candidates
            @self.pc.on("icecandidate")
            async def on_icecandidate(candidate):
                if candidate:
                    message = {
                        'id': 'onIceCandidate',
                        'candidate': candidate.toJSON()
                    }
                    await self.send_message(message)
                    logger.info(f"Sent ICE candidate: {candidate}")

        except Exception as error:
            logger.error(f"Failed to connect to WebSocket server: {error}")

    async def send_message(self, message):
        """Send a message over the WebSocket connection."""
        json_message = json.dumps(message)
        try:
            await self.websocket.send(json_message)
            logger.info(f"Sent message: {json_message}")
        except Exception as error:
            logger.error(f"Failed to send WebSocket message ({self.type}): {error}")

    async def generate_local_description(self):
        """Generate and return the local SDP description."""
        for transceiver in self.pc.getTransceivers():
            if transceiver.kind == "video":
                video_transceiver = transceiver
                break
        else:
            raise ValueError("No video transceiver found")

            # Get available codecs
        capabilities = RTCRtpSender.getCapabilities("video")
        available_codecs = capabilities.codecs

        # Define the codecs you want to use, in order of preference
        preferred_codec_names = ["VP8", "H264", "VP9"]

        # Filter and order codecs based on preferences and availability
        preferred_codecs = []
        for codec_name in preferred_codec_names:
            for available_codec in available_codecs:
                if codec_name in available_codec.mimeType:
                    preferred_codecs.append(available_codec)
                    break

        if not preferred_codecs:
            raise ValueError("No preferred codecs are available")

        # Set the codec preferences
        video_transceiver.setCodecPreferences(preferred_codecs)

        offer = await self.pc.createOffer()
        await self.pc.setLocalDescription(offer)
        await self.wait_for_ice_gathering()
        logger.info(f"Generated local description: {self.pc.localDescription.sdp}")
        return self.pc.localDescription

    async def wait_for_ice_gathering(self):
        """Wait for ICE gathering to complete."""
        await asyncio.sleep(0.5)  # Small delay to ensure ICE candidates are gathered
        while True:
            connection_state = self.pc.iceConnectionState
            gathering_state = self.pc.iceGatheringState
            logger.debug(f"ICE connection state: {connection_state}, ICE gathering state: {gathering_state}")
            if gathering_state == "complete":
                break
            await asyncio.sleep(0.1)

    async def send_local_description(self):
        """Send the local SDP description to the WebSocket server."""
        local_description = await self.generate_local_description()
        sdp = modify_sdp(local_description.sdp)
        message = {
            "id": self.id,
            "type": self.type,
            "contentType": self.contentType,
            "role": self.role,
            "internalMeetingId": self.internalMeetingId,
            "voiceBridge": self.voiceBridge,
            "userName": self.userName,
            "callerName": self.callerName,
            "sdpOffer": sdp,
            "hasAudio": self.hasAudio,
            "bitrate": self.bitrate
        }
        ping = {"id": "ping"}
        await self.send_message(ping)
        await self.send_message(message)

    async def receive_messages(self):
        try:
            async for message in self.websocket:
                logger.info(f"Received message: {message}")
                await self.handle_message(message)
                data = ast.literal_eval(message)
                if data.get('id') == 'playStart':
                    self.screen_sharing = True
                    # Start a continuous capture loop
                    await asyncio.create_task(self.capture_loop())
        except Exception as error:
            logger.error(f"Error receiving messages: {error}")
        finally:
            await self.websocket.close()
            logger.info("WebSocket connection closed")

    async def handle_message(self, message):
        data = json.loads(message)
        logger.info(f"Handling message: {data}")

        if data['id'] == 'pong':
            logger.info("Received pong message")
        elif data['id'] == 'startResponse' and data['response'] == 'accepted':
            sdp_answer = RTCSessionDescription(sdp=data['sdpAnswer'], type='answer')
            await self.pc.setRemoteDescription(sdp_answer)
            logger.info(f"Set remote description: {sdp_answer}")
        elif data['id'] == 'iceCandidate':
            candidate = RTCIceCandidate(
                sdpMid=data['candidate']['sdpMid'],
                sdpMLineIndex=data['candidate']['sdpMLineIndex'],
                candidate=data['candidate']['candidate']
            )
            await self.pc.addIceCandidate(candidate)
            logger.info(f"Added remote ICE candidate: {candidate}")

    def _parse_turn_servers(self):
        """Parse and return the TURN server configurations."""
        ice_servers = []
        for turn_server in self.turn_servers:
            ice_servers.append(RTCIceServer(
                urls=[turn_server["url"]],
                username=turn_server["username"],
                credential=turn_server["password"]
            ))
        return ice_servers

    async def stop(self):
        """Stop the screenshare session."""
        if self.status == 'MEDIA_STOPPED':
            logger.warn('Screenshare session already stopped')
            return

        if self.status == 'MEDIA_STOPPING':
            logger.warn('Screenshare session already stopping')
            await self.wait_until_stopped()
            logger.info('Screenshare delayed stop resolution for queued stop call')
            return

        if self.status == 'MEDIA_STARTING':
            logger.warn('Screenshare session still starting on stop, wait.')
            if not self._stopActionQueued:
                self._stopActionQueued = True
                await self.wait_until_negotiated()
                logger.info('Screenshare delayed MEDIA_STARTING stop resolution')
                await self.stop_presenter()
            else:
                await self.wait_until_stopped()
                logger.info('Screenshare delayed stop resolution for queued stop call')
            return

        await self.stop_presenter()

    async def wait_until_stopped(self):
        """Wait until the media is stopped."""
        while self.status != 'MEDIA_STOPPED':
            await asyncio.sleep(0.1)

    async def wait_until_negotiated(self):
        """Wait until the media is negotiated."""
        while self.status != 'MEDIA_NEGOTIATED':
            await asyncio.sleep(0.1)

    async def stop_presenter(self):
        """Stop the presenter and handle errors."""
        try:
            # Add your logic to stop the presenter
            self.status = 'MEDIA_STOPPING'
            # Simulate stopping action
            await asyncio.sleep(1)  # Simulate delay
            self.status = 'MEDIA_STOPPED'
            logger.info('Screenshare stopped successfully')
        except Exception as error:
            logger.error(f'Screenshare stop failed: {error}')
            self.status = 'MEDIA_STOPPED'

    async def restart_ice(self):
        pass

    # async def start_screen_share(self):
    #     logger.info("Starting screen share")
    #     try:
    #         stream = ScreenShareTrack()
    #         sender = self.pc.addTrack(stream)
    #         logger.info(f"Added screen share track to peer connection: {sender}")
    #         await self.send_local_description()
    #         await asyncio.create_task(stream.recv())
    #         logger.info("Screen share started successfully")
    #     except Exception as e:
    #         logger.error(f"Error starting screen share: {e}")
    async def start_screen_share(self):

        logger.info("Starting screen share")
        try:
            self.screen_share_track = ScreenShareTrack()
            self.screen_share_sender = self.pc.addTrack(self.screen_share_track)
            logger.info(f"Added screen share track to peer connection: {self.screen_share_sender}")

            await self.send_local_description()
            await self.receive_messages()
            # Create a flag to control the loop
            await self.screen_share_track.capture_frame()


            logger.info("Screen share started successfully")
        except Exception as e:
            logger.error(f"Error starting screen share: {e}")

    async def capture_loop(self):
        while self.screen_sharing:
            try:
                await self.screen_share_track.recv()
                await asyncio.sleep(1 / 30)  # Adjust this value to control frame rate
            except Exception as e:
                logger.error(f"Error in screen capture loop: {e}")
                break  # Exit the loop on error

        logger.info("Screen sharing stopped")

    async def stop_screen_share(self):
        self.screen_sharing = False
        # Remove the track from the peer connection
        self.pc.removeTrack(self.screen_share_sender)
        # Close the screen share track if it has a close method
        if hasattr(self.screen_share_track, 'close'):
            await self.screen_share_track.close()
        self.screen_share_track = None
        self.screen_share_sender = None