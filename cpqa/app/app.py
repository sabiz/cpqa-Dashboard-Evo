from cpqa.common import log_init
from cpqa.common import log_d
from cpqa.common import log_i
from cpqa.common import Settings
from cpqa.common import Keys
from cpqa.app.scene import SceneDirector
from cpqa.app.core import Scheduler
from cpqa.app.core import FrameRate
from cpqa.app.core import Screen
from cpqa.mut import MutClient

LOG_TAG = "CpqaDashboard"


class CpqaDashboard:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__settings = Settings()
        self.__settings.load()
        log_init()
        self.__need_exit = False
        log_d(LOG_TAG, "Init CpqaDashboard")

        self.__scene_director = SceneDirector()
        use_mock = self.__settings.get(Keys.USE_MOCK)
        log_i(LOG_TAG, f"use_mock: {use_mock}")
        self.__mut_client = MutClient(use_mock)
        self.__scheduler = Scheduler()

    def run(self):
        log_i(LOG_TAG, "CpqaDashboard Run")

        frame_rate = FrameRate()
        screen = Screen()
        while not self.__need_exit:
            self.__scheduler.tick()
            self.__scene_director.update(self.__mut_client)
            self.__need_exit = screen.update(
                lambda canvas: self.__scene_director.draw(canvas)
            )
            self.__scene_director.change_scene_if_needed(self.__mut_client)
            frame_rate.wait()
        log_i(LOG_TAG, "CpqaDashboard Exit")
