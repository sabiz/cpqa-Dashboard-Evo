import pyray as pr
from ._null_scene import NullScene
from ._initializing_scene import InitializingScene
from ._main_scene import MainScene
from ._exit_scene import ExitScene
from cpqa.common import log_d
from cpqa.common import log_i

LOG_TAG = "SceneDirector"


class SceneDirector:
    def __init__(self):
        self.__scene = NullScene
        self.__scene_dict = {
            NullScene: NullScene(),
            InitializingScene: InitializingScene(),
            MainScene: MainScene(),
            ExitScene: ExitScene(),
        }

    def update(self, mut_client):
        # log_d(LOG_TAG, f"SceneDirector Update: {self.__scene}")
        scene = self.__get_current_scene()
        scene.update(mut_client)

    def draw(self):
        # log_d(LOG_TAG, f"SceneDirector Draw: {self.__scene}")
        scene = self.__get_current_scene()
        pr.begin_drawing()
        scene.draw()
        pr.draw_fps(0, 0)
        pr.end_drawing()

    def change_scene_if_needed(self, mut_client):
        next_scene = self.__get_current_scene().change_scene_if_needed(mut_client)
        if next_scene is None:
            return
        log_i(LOG_TAG, f"Change scene to {next_scene}")
        self.__get_current_scene().on_exit(mut_client)
        self.__scene = next_scene
        self.__get_current_scene().on_enter(mut_client)

    def __get_current_scene(self):
        scene = self.__scene_dict[self.__scene]
        if scene is None:
            raise ValueError("Invalid scene")
        return scene
