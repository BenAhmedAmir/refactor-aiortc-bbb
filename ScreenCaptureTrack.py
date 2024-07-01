import asyncio
import time

import mss
import numpy as np
from aiortc import VideoStreamTrack
from av import VideoFrame
from av.frame import Frame

from Logger import configure_logger

logger = configure_logger()


class ScreenShareTrack(VideoStreamTrack):
    kind = "video"

    def __init__(self, fps=30, width=None, height=None):
        super().__init__()
        self.fps = fps
        self.width = width
        self.height = height
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]  # Capture the primary monitor
        self.monitor = {"top": 50, "left": 250, "width": 800, "height": 600}
        self.frame_rate = 1 / self.fps
        self._last_frame_time = 0
        print('outside')

    # def set_capture_area(self, rect):
    #     self.monitor = {"top": rect.top(), "left": rect.left(), "width": rect.width(), "height": rect.height()}


    async def recv(self):
        pts, time_base = await self.next_timestamp()
        print('salem')
        now = time.time()
        if now - self._last_frame_time < self.frame_rate:
            await asyncio.sleep(self.frame_rate - (now - self._last_frame_time))
        self._last_frame_time = time.time()

        frame = np.array(self.sct.grab(self.monitor))
        frame = VideoFrame.from_ndarray(frame, format="bgra")
        frame.pts = pts
        frame.time_base = time_base
        return frame


async def attempt_connection(ws_client):
    """Attempt to connect and establish a WebRTC connection with retries."""
    # await ws_client.connect()
    video_track = ScreenShareTrack()
    ws_client.pc.addTrack(video_track)

    # Create SDP offer and set local description
    # await generate_local_description(ws_client.pc)

    await ws_client.send_local_description()
    await ws_client.receive_messages()
    logger.error("All attempts to establish connection failed")
