import sys
from cpqa.app.core import Painter
from cpqa.common import log_d
from ._scene_interface import SceneInterface


class ExitScene(SceneInterface):
    def update(self, mut_client):
        pass

    def draw(self, canvas):
        Painter.clear(canvas)

    def change_scene_if_needed(self, mut_client):
        pass

    def on_enter(self, mut_client):
        log_d("ExitScene", "Exiting...")
        sys.exit()

    def on_exit(self, mut_client):
        pass
