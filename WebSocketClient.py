import asyncio
import json

import websockets
from aiortc import RTCPeerConnection, RTCConfiguration, RTCSessionDescription, RTCIceCandidate, RTCIceServer
from Logger import configure_logger

logger = configure_logger()


class WebSocketClient:
    def __init__(self, turns_servers, **kwargs):
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
        self.turn_servers = json.loads(kwargs.get("turn_servers"))
        self.ws_url = kwargs.get("ws_url")
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
            logger.error(f"Failed to send WebSocket message ({self.sfu_component}): {error}")

    async def generate_local_description(self):
        """Generate and return the local SDP description."""
        await self.pc.setLocalDescription(await self.pc.createOffer())
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
        message = {
            "id": self.id,
            "type": self.type,
            "contentType": self.contentType,
            "role": self.role,
            "internalMeetingId": self.internalMeetingId,
            "voiceBridge": self.voiceBridge,
            "userName": self.userName,
            "callerName": self.callerName,
            "sdpOffer": local_description.sdp,
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
