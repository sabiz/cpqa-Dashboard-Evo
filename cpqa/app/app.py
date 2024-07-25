import pyray as pr
from cpqa.common import log_init
from cpqa.common import log_d
from cpqa.common import log_i
from cpqa.common import Settings
from cpqa.common import Keys
from cpqa.app.scene import SceneDirector
from cpqa.app.core import Scheduler
from cpqa.mut import MutClient

LOG_TAG = "CpqaDashboard"
FPS = 15


class CpqaDashboard:
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__settings = Settings()
        self.__settings.load()
        log_init()
        log_d(LOG_TAG, "Init CpqaDashboard")

        self.__scene_director = SceneDirector()
        use_mock = self.__settings.get(Keys.USE_MOCK)
        log_i(LOG_TAG, f"use_mock: {use_mock}")
        self.__mut_client = MutClient(use_mock)
        self.__scheduler = Scheduler()

    def run(self):
        log_i(LOG_TAG, "CpqaDashboard Run")
        width = self.__settings.get(Keys.WINDOW_WIDTH)
        height = self.__settings.get(Keys.WINDOW_HEIGHT)
        pr.init_window(width, height, "Cpqa-Dashboard-Evo")
        pr.set_target_fps(FPS)

        while not pr.window_should_close():
            self.__scheduler.tick()
            self.__scene_director.update(self.__mut_client)
            self.__scene_director.draw()
            self.__scene_director.change_scene_if_needed(self.__mut_client)
        pr.close_window()
        log_i(LOG_TAG, "CpqaDashboard Exit")
