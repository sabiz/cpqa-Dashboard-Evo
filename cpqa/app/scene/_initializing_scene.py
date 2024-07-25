import pyray as pr
from ._scene_interface import SceneInterface
from ._main_scene import MainScene
from cpqa.app.core import Scheduler
from cpqa.app.util.graphics_util import get_ajusted_font_size
from cpqa.common import log_d
from cpqa.common import log_i
from cpqa.common import Settings
from cpqa.common import Keys

LOG_TAG = "InitializingScene"


class InitializingScene(SceneInterface):
    TEXT = "Initializing..."
    ZERO_VECTOR2 = pr.Vector2(0, 0)
    COLOR_TABLE_UPPER = [
        pr.Color(180, 180, 180, 255),
        pr.Color(180, 180, 12, 255),
        pr.Color(13, 180, 180, 255),
        pr.Color(13, 180, 12, 255),
        pr.Color(180, 16, 180, 255),
        pr.Color(180, 15, 14, 255),
        pr.Color(15, 15, 180, 255),
    ]
    COLOR_TABLE_MIDDLE = [
        pr.Color(15, 15, 180, 255),
        pr.Color(16, 16, 16, 255),
        pr.Color(180, 16, 180, 255),
        pr.Color(16, 16, 16, 255),
        pr.Color(13, 180, 180, 255),
        pr.Color(16, 16, 16, 255),
        pr.Color(180, 180, 180, 255),
    ]
    COLOR_TABLE_BOTTOM_LEFT = [
        pr.Color(8, 29, 66, 255),
        pr.Color(235, 235, 235, 255),
        pr.Color(44, 0, 92, 255),
        pr.Color(16, 16, 16, 255),
    ]
    COLOR_TABLE_BOTTOM_MIDDLE = [
        pr.Color(7, 7, 7, 255),
        pr.Color(16, 16, 16, 255),
        pr.Color(24, 24, 24, 255),
    ]
    COLOR_BOTTOM_RIGHT = pr.Color(16, 16, 16, 255)

    def __init__(self):
        self.__scheduler = Scheduler()
        self.__settings = Settings()
        self.__screen_width = None
        self.__screen_height = None
        self.__font_size = None
        self.__text_y_pos = None
        self.__bar_rectangle_upper_list = []
        self.__bar_rectangle_middle_list = []
        self.__bar_rectangle_bottom_left_list = []
        self.__bar_rectangle_bottom_middle_list = []
        self.__bar_rectangle_bottom_right = None
        self.__is_opened = False

    def update(self, mut_client):
        pass

    def draw(self):
        pr.clear_background(pr.BLACK)
        # draw SMPTE color bars
        for i, rect in enumerate(self.__bar_rectangle_upper_list):
            pr.draw_rectangle_pro(
                rect,
                InitializingScene.ZERO_VECTOR2,
                0,
                InitializingScene.COLOR_TABLE_UPPER[i],
            )
        for i, rect in enumerate(self.__bar_rectangle_middle_list):
            pr.draw_rectangle_pro(
                rect,
                InitializingScene.ZERO_VECTOR2,
                0,
                InitializingScene.COLOR_TABLE_MIDDLE[i],
            )
        for i, rect in enumerate(self.__bar_rectangle_bottom_left_list):
            pr.draw_rectangle_pro(
                rect,
                InitializingScene.ZERO_VECTOR2,
                0,
                InitializingScene.COLOR_TABLE_BOTTOM_LEFT[i],
            )
        for i, rect in enumerate(self.__bar_rectangle_bottom_middle_list):
            pr.draw_rectangle_pro(
                rect,
                InitializingScene.ZERO_VECTOR2,
                0,
                InitializingScene.COLOR_TABLE_BOTTOM_MIDDLE[i],
            )
        pr.draw_rectangle_pro(
            self.__bar_rectangle_bottom_right,
            InitializingScene.ZERO_VECTOR2,
            0,
            InitializingScene.COLOR_BOTTOM_RIGHT,
        )

        # Draw text
        pr.draw_text(
            InitializingScene.TEXT,
            5,
            self.__text_y_pos,
            self.__font_size,
            pr.WHITE,
        )

    def change_scene_if_needed(self, mut_client):
        if self.__is_opened:
            return MainScene
        return None

    def on_enter(self, mut_client):
        if self.__screen_width is None or self.__screen_height is None:
            self.__screen_width = pr.get_screen_width()
            self.__screen_height = pr.get_screen_height()
            self.__font_size = get_ajusted_font_size(
                InitializingScene.TEXT, self.__screen_width
            )
            self.__text_y_pos = (self.__screen_height - self.__font_size) // 2
            bar_upper_width = self.__screen_width / len(
                InitializingScene.COLOR_TABLE_UPPER
            )
            bar_upper_height = self.__screen_height * (2 / 3)
            self.__bar_rectangle_upper_list = []
            for i in range(len(InitializingScene.COLOR_TABLE_UPPER)):
                self.__bar_rectangle_upper_list.append(
                    pr.Rectangle(
                        i * bar_upper_width, 0, bar_upper_width, bar_upper_height
                    )
                )
            bar_middle_width = self.__screen_width / len(
                InitializingScene.COLOR_TABLE_MIDDLE
            )
            bar_middle_height = self.__screen_height * (1 / 12)
            self.__bar_rectangle_middle_list = []
            for i in range(len(InitializingScene.COLOR_TABLE_MIDDLE)):
                self.__bar_rectangle_middle_list.append(
                    pr.Rectangle(
                        i * bar_middle_width,
                        bar_upper_height,
                        bar_middle_width,
                        bar_middle_height,
                    )
                )
            bar_bottom_left_width = (self.__screen_width * (5 / 7)) / len(
                InitializingScene.COLOR_TABLE_BOTTOM_LEFT
            )
            bar_bottom_left_height = self.__screen_height * (1 / 4)
            self.__bar_rectangle_bottom_left_list = []
            for i in range(len(InitializingScene.COLOR_TABLE_BOTTOM_LEFT)):
                self.__bar_rectangle_bottom_left_list.append(
                    pr.Rectangle(
                        i * bar_bottom_left_width,
                        bar_upper_height + bar_middle_height,
                        bar_bottom_left_width,
                        bar_bottom_left_height,
                    )
                )
            bar_bottom_middle_width = bar_upper_width / len(
                InitializingScene.COLOR_TABLE_BOTTOM_MIDDLE
            )
            bar_bottom_middle_height = self.__screen_height * (1 / 4)
            self.__bar_rectangle_bottom_middle_list = []
            for i in range(len(InitializingScene.COLOR_TABLE_BOTTOM_MIDDLE)):
                self.__bar_rectangle_bottom_middle_list.append(
                    pr.Rectangle(
                        i * bar_bottom_middle_width + (self.__screen_width * (5 / 7)),
                        bar_upper_height + bar_middle_height,
                        bar_bottom_middle_width,
                        bar_bottom_middle_height,
                    )
                )
            self.__bar_rectangle_bottom_right = pr.Rectangle(
                self.__screen_width - bar_upper_width,
                bar_upper_height + bar_middle_height,
                bar_upper_width,
                bar_bottom_middle_height,
            )

        self.__scheduler.add_next_tick(self.__find_device(mut_client))

    def on_exit(self, mut_client):
        pass

    def __find_device(self, mut_client):
        def find_device_impl():
            log_d(LOG_TAG, "Find Device")
            # Waiting for device connection
            if not mut_client.exist_device():
                log_i(LOG_TAG, "Device not found")
                self.__scheduler.add_after(find_device_impl, 300)
                return
            self.__scheduler.add_after(self.__open_device(mut_client), 300)

        return find_device_impl

    def __open_device(self, mut_client):
        device_index = self.__settings.get(Keys.DEVICE_INDEX)
        log_d(LOG_TAG, f"device_index: {device_index}")

        def open_device_impl():
            log_i(LOG_TAG, "Open Device")
            result = mut_client.open(device_index)
            if result.is_success:
                self.__is_opened = True
            else:
                log_i(LOG_TAG, "retry to open device")
                self.__scheduler.add_after(self.__find_device(mut_client), 300)

        return open_device_impl
