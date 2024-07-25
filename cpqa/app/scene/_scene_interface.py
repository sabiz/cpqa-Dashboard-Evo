from abc import ABCMeta
from abc import abstractmethod


class SceneInterface(metaclass=ABCMeta):
    @abstractmethod
    def update(self, mut_client):
        pass

    @abstractmethod
    def draw(self):
        pass

    @abstractmethod
    def change_scene_if_needed(self, mut_client):
        pass

    @abstractmethod
    def on_enter(self, mut_client):
        pass

    @abstractmethod
    def on_exit(self, mut_client):
        pass
