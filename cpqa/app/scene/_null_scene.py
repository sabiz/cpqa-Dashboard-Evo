import pyray as pr
from ._scene_interface import SceneInterface
from ._initializing_scene import InitializingScene


class NullScene(SceneInterface):
    def update(self, mut_client):
        pass

    def draw(self):
        pr.clear_background(pr.BLACK)

    def change_scene_if_needed(self, mut_client):
        return InitializingScene

    def on_enter(self, mut_client):
        pass

    def on_exit(self, mut_client):
        pass
