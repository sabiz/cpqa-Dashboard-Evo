from ._scene_interface import SceneInterface
from ._initializing_scene import InitializingScene
from cpqa.app.core import Painter


class NullScene(SceneInterface):
    def update(self, mut_client):
        pass

    def draw(self, canvas):
        Painter.clear(canvas)

    def change_scene_if_needed(self, mut_client):
        return InitializingScene

    def on_enter(self, mut_client):
        pass

    def on_exit(self, mut_client):
        pass
