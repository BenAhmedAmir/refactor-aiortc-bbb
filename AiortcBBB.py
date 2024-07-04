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
    parser.add_argument("--internalMeetingId", type=str, required=True, help="Internal MeetingId")
    parser.add_argument("--userName", type=str, required=True, help="User name")
    parser.add_argument("--callerName", type=str, required=True, help="Caller Name")
    parser.add_argument("--cookies", type=str, required=True, help="Cookies for WebSocket connection")
    # parser.add_argument("--turn_servers", type=str, required=True, help="TURN servers in JSON format")

    args = parser.parse_args()

    # Convert TURN servers from JSON string to Python list
    try:
        turn_servers = json.loads('[{"username": "1720185359:w_4ubm1haud4ey","password": "qYMsTxsddP+QKCZdhxwHU9YBFpM=","url": "turn:bbb.ostedhy.tn:3478","ttl": 86400}]')
    except json.JSONDecodeError as e:
        print(f"Invalid TURN servers JSON: {e}")
        return

    # Create a dictionary of arguments
    ws_client_args = {
        "ws_url": args.ws_url,
        "sfu_component": args.sfu_component,
        "role": args.role,
        "voiceBridge": args.voice_bridge,
        "internalMeetingId": args.internalMeetingId,
        "userName": args.userName,
        "callerName": args.callerName,
        "cookies": args.cookies,
        "turn_servers": turn_servers
    }

    # Initialize and connect WebSocketClient
    ws_client = WebSocketClient(**ws_client_args)
    await ws_client.connect()

    # Attempt connection (assuming this sets up the media track)
    await attempt_connection(ws_client)

    # Start receiving messages
    await ws_client.receive_messages()

if __name__ == "__main__":
    # asyncio.run(main())
    asyncio.get_event_loop().run_until_complete(main())