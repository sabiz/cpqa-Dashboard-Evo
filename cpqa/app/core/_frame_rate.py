import time
from cpqa.common import log_d

TARGET_FPS = 15

LOG_TAG = "FrameRate"


class FrameRate:
    def __init__(self):
        self.__target_fps = TARGET_FPS
        self.__frame_time = 1.0 / self.__target_fps
        self.__last_time = 0.0

    def wait(self):
        current_time = time.time()
        elapsed_time = current_time - self.__last_time
        sleep_time = self.__frame_time - elapsed_time
        # log_d(LOG_TAG, f"sleep_time: {sleep_time}")
        if sleep_time > 0:
            time.sleep(sleep_time)
        self.__last_time = time.time()
