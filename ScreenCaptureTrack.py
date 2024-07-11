import asyncio
import time

import cv2
import mss
import numpy
import numpy as np
from aiortc import VideoStreamTrack
from av import VideoFrame
import tkinter as tk

from Logger import configure_logger

logger = configure_logger()


# screen_width, screen_height = get_screen_size()


class ScreenShareTrack(VideoStreamTrack):
    kind = "video"

    def __init__(self, fps=30, width=None, height=None):
        super().__init__()
        self.fps = fps
        self.width = width
        self.height = height
        self.sct = mss.mss()
        self.monitor = self.sct.monitors[1]
        self.monitor = {"top": 50, "left": 250, "width": 800, "height": 600}
        self.frame_interval = 1 / self.fps
        self._last_frame_time = 0
        self.frame_count = 0

    async def recv(self):
        frame = await self.capture_frame()
        self.frame_count += 1
        if self.frame_count % 30 == 0:  # Log every 30 frames
            logger.info(f"Captured frame {self.frame_count}")
        return frame

    async def capture_frame(self, output_format="bgr24"):
        pts, time_base = await self.next_timestamp()

        now = time.time()
        if now - self._last_frame_time < self.frame_interval:
            await asyncio.sleep(self.frame_interval - (now - self._last_frame_time))
        self._last_frame_time = time.time()

        frame = np.array(self.sct.grab(self.monitor))

        # Remove alpha channel if present
        if frame.shape[2] == 4:
            frame = frame[:, :, :3]

        if output_format == "bgr24":
            # MSS captures in BGR format, so we can use it directly
            pass
        elif output_format == "rgb24":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        elif output_format in ["yuv420p", "yuvj420p", "yuv422p", "yuv444p"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV)
        elif output_format == "nv12":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_I420)
        elif output_format == "nv21":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2YUV_YV12)
        elif output_format == "gray":
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        elif output_format in ["rgba", "bgra"]:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA if output_format == "rgba" else cv2.COLOR_BGR2BGRA)
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        frame = VideoFrame.from_ndarray(frame, format=output_format)
        frame.pts = pts
        frame.time_base = time_base
        return frame

    async def close(self):
        self.sct.close()
