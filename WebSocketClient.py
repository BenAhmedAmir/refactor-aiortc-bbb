import asyncio
import json
import websockets
from aiortc import RTCPeerConnection, RTCConfiguration, RTCSessionDescription, RTCIceCandidate, RTCIceServer, \
    RTCRtpCodecParameters, RTCRtpCodecCapability, RTCRtpCapabilities
from Logger import configure_logger

logger = configure_logger()


def modify_sdp(sdp):
    # Split SDP into lines for easier manipulation
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
        offer_options = {
            'offerToReceiveAudio': False,
            'offerToReceiveVideo': False
        }
        video_transceiver = self.pc.getTransceivers()[0]
        capabilities = RTCRtpCapabilities(codecs=video_transceiver.sender.getCapabilities("video").codecs)
        desired_codecs = [
            RTCRtpCodecParameters(mimeType="video/VP8", clockRate=90000),
            RTCRtpCodecParameters(mimeType="video/H264", clockRate=90000, parameters={"profile-level-id": "42e01f"}),
            RTCRtpCodecParameters(mimeType="video/H264", clockRate=90000, parameters={"profile-level-id": "42001f"}),
            RTCRtpCodecParameters(mimeType="video/VP9", clockRate=90000),
            RTCRtpCodecParameters(mimeType="video/AV1", clockRate=90000),
        ]
        print(desired_codecs)
        supported_codecs = [codec for codec in desired_codecs if codec in capabilities.codecs]

        # video_transceiver.setCodecPreferences(supported_codecs)
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
        """Receive and handle messages from the WebSocket server."""
        logger.info("Start receiving messages")
        try:
            async for message in self.websocket:
                logger.info(f"Received message: {message}")
                await self.handle_message(message)
        except Exception as error:
            logger.error(f"Error receiving messages: {error}")
        finally:
            await self.websocket.close()
            logger.info("WebSocket connection closed")

    async def handle_message(self, message):
        """Handle incoming messages from the WebSocket server."""
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


media_constraints = {
    'audio': False,  # Disable audio for sender-only
    'video': {
        'mandatory': [{'width': 640}, {'height': 360}],  # Example resolution
        'optional': [{'goog-codec': 'vp8'}, {'goog-codec': 'h264'}, {'goog-codec': 'av1'}]  # Example codecs
    }
}
