import asyncio
import time

import cv2
import mss
import numpy as np
from aiortc import VideoStreamTrack
from aiortc.mediastreams import MediaStreamError
from av import VideoFrame
from Logger import configure_logger
logger = configure_logger()


class ScreenShareTrack(VideoStreamTrack):
    kind = "video"
    print("salem 1")

    def __init__(self, fps=30):
        super().__init__()
        self.fps = fps
        self.sct = mss.mss()

    print("salem 2")

    async def recv(self):
        pts, time_base = await self.next_timestamp()
        # Capture the screen
        monitor = self.sct.monitors[1]  # Change the monitor index if needed
        frame = np.array(self.sct.grab(monitor))
        print(frame)
        # Convert the frame to the format expected by aiortc
        frame = VideoFrame.from_ndarray(frame, format="bgra")
        frame.pts = pts
        frame.time_base = time_base

        return frame




async def attempt_connection(ws_client):
    """Attempt to connect and establish a WebRTC connection with retries."""
    await ws_client.connect()
    ws_client.keep_alive_task = asyncio.create_task(ws_client.keep_alive())
    video_track = ScreenShareTrack()
    ws_client.pc.addTrack(video_track)

    # Create SDP offer and set local description
    # await generate_local_description(ws_client.pc)

    await ws_client.send_local_description()
    await ws_client.receive_messages()
    logger.error("All attempts to establish connection failed")
    # try:
    #     await ws_client.connect()
    #     video_track = ScreenShareTrack()
    #     ws_client.pc.addTransceiver(video_track, direction='sendonly')
    #     await ws_client.send_local_description()
    #     await ws_client.receive_messages()
    # except Exception as e:
    #     logger.error(f"Failed to establish WebRTC connection: {e}")
    #

