import argparse
import asyncio
import json
import signal
import sys

from WebSocketClient import WebSocketClient
from Logger import configure_logger

logger = configure_logger()

parser = argparse.ArgumentParser(description="WebRTC Screen Sharing Client")
parser.add_argument("--ws_url", type=str, required=True, help="WebSocket URL")
parser.add_argument("--sfu_component", type=str, required=True, help="SFU component")
parser.add_argument("--role", type=str, required=True, help="Role (send/receive)")
parser.add_argument("--voice_bridge", type=str, required=True, help="Voice bridge")
parser.add_argument("--internalMeetingId", type=str, required=True, help="Internal MeetingId")
parser.add_argument("--userName", type=str, required=True, help="User name")
parser.add_argument("--callerName", type=str, required=True, help="Caller Name")
# parser.add_argument("--cookies", type=str, required=True, help="Cookies for WebSocket connection")
# parser.add_argument("--turn_servers", type=str, required=True, help="TURN servers in JSON format")
args = parser.parse_args()

try:
    turn_servers = json.loads('[{"username": "1722410059:w_saduaq0sx7nq","password": "AC5GX8vs5+9D/D+i7fUNQajvtvU=","url": "turn:bbb.ostedhy.tn:3478","ttl": 8640}]')
except json.JSONDecodeError as e:
    print(f"Invalid TURN servers JSON: {e}")
    sys.exit(1)

ws_client_args = {
    "ws_url": args.ws_url,
    "sfu_component": args.sfu_component,
    "role": args.role,
    "voiceBridge": args.voice_bridge,
    "internalMeetingId": args.internalMeetingId,
    "userName": args.userName,
    "callerName": args.callerName,
    # "cookies": args.cookies,
    "turn_servers": turn_servers
}

ws_client = WebSocketClient(**ws_client_args)


async def attempt_connection(client):
    """Attempt to connect and establish a WebRTC connection with retries."""
    await ws_client.receive_messages()
    logger.error("All attempts to establish connection failed")


async def main():
    await ws_client.connect()
    await asyncio.sleep(2)
    await ws_client.start_screen_share()



    await ws_client.receive_messages()


async def async_signal_handler():
    logger.info("Received termination signal. Stopping the project...")
    await ws_client.stop()
    sys.exit(0)


def signal_handler(signal, frame):
    asyncio.create_task(async_signal_handler())


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error(f"Exception in main event loop")
        print('keyboard interrupt')
