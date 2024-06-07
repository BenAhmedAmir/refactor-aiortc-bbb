import argparse
import asyncio
import json

from WebSocketClient import WebSocketClient
from ScreenCaptureTrack import attempt_connection


async def main():
    parser = argparse.ArgumentParser(description="WebRTC Screen Sharing Client")
    parser.add_argument("--ws_url", type=str, required=True, help="WebSocket URL")
    parser.add_argument("--sfu_component", type=str, required=True, help="SFU component")
    parser.add_argument("--role", type=str, required=True, help="Role (send/receive)")
    parser.add_argument("--voice_bridge", type=str, required=True, help="Voice bridge")
    parser.add_argument("--internalMeetingId", type=str, required=True, help="internal MeetingId")
    parser.add_argument("--userName", type=str, required=True, help="user name")
    parser.add_argument("--callerName", type=str, required=True, help="caller Name")
    parser.add_argument("--cookies", type=str, required=True, help="Cookies for WebSocket connection")
    parser.add_argument("--turn_servers", type=str, required=True, help="TURN servers in JSON format")

    args = parser.parse_args()

    ws_client = WebSocketClient(args)
    await attempt_connection(ws_client)


if __name__ == "__main__":
    asyncio.run(main())
