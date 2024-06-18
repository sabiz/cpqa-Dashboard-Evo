import os
from pathlib import Path
from kivy.uix.image import Image


class PowerButton(Image):

    def __init__(self, **kwargs):
        image_path = ((Path(__file__).parent.parent
                      .parent.parent / 'res' / 'power_button.png').absolute())
        super().__init__(source=str(image_path), **kwargs)
        self.__command = "echo"
        self.__before_callback = None

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self.__before_callback is not None:
            self.__before_callback()
        os.system(self.__command)

    def set_command(self, cmd):
        self.__command = cmd

    def set_before_callback(self, callback):
        self.__before_callback = callback
