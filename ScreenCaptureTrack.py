import asyncio
import time

import mss
import numpy as np
from aiortc import VideoStreamTrack
from av import VideoFrame
from Logger import configure_logger

logger = configure_logger()


class ScreenCaptureTrack(VideoStreamTrack):
    kind = "video"

    def __init__(self, fps=30):
        super().__init__()
        self.fps = fps
        self.sct = mss.mss()
        self.monitor = {"top": 50, "left": 250, "width": 800, "height": 600}
        self.frame_rate = 1 / self.fps
        self._last_frame_time = 0

    def set_capture_area(self, rect):
        """Set the capture area for screen capture."""
        self.monitor = {"top": rect.top(), "left": rect.left(), "width": rect.width(), "height": rect.height()}

    async def recv(self):
        """Capture and return the next video frame."""
        pts, time_base = await self.next_timestamp()
        now = time.time()
        if now - self._last_frame_time < self.frame_rate:
            await asyncio.sleep(self.frame_rate - (now - self._last_frame_time))
        self._last_frame_time = time.time()

        frame = np.array(self.sct.grab(self.monitor))
        frame = VideoFrame.from_ndarray(frame, format="bgra")
        frame.pts = pts
        frame.time_base = time_base
        return frame


async def attempt_connection(ws_client, attempts=1, delay=2):
    """Attempt to connect and establish a WebRTC connection with retries."""
    for attempt in range(attempts):
        try:
            await ws_client.connect()
            ws_client.pc.addTrack(ScreenCaptureTrack())
            await ws_client.send_local_description()
            await ws_client.receive_messages()
            return
        except Exception as e:
            logger.error(f"Attempt {attempt + 1}/{attempts} failed: {e}")
            await asyncio.sleep(delay)
    logger.error("All attempts to establish connection failed")
