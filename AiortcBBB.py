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
    parser.add_argument("--cookies", type=str, required=True, help="Cookies for WebSocket connection")
    parser.add_argument("--turn_servers", type=str, required=True, help="TURN servers in JSON format")

    args = parser.parse_args()

    turn_servers = json.loads(args.turn_servers)

    ws_client = WebSocketClient(
        ws_url=args.ws_url,
        log_code_prefix=args.log_code_prefix,
        sfu_component=args.sfu_component,
        role=args.role,
        voice_bridge=args.voice_bridge,
        user_id=args.user_id,
        cookies=args.cookies,
        turn_servers=turn_servers,
        id="start",
        type="screenshare",
        contentType="screenshare",
        internalMeetingId=args.internalMeetingId,
        userName=args.userName,
        callerName="w_8fwydohzamj3",
        hasAudio=False,
        bitrate=1500
    )
    await attempt_connection(ws_client)


if __name__ == "__main__":
    asyncio.run(main())
