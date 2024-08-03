from ._scene_interface import SceneInterface
from ._main_scene import MainScene
from cpqa.app.core import Scheduler
from cpqa.app.core import Painter
from cpqa.app.core import Rectangle
from cpqa.common import log_d
from cpqa.common import log_i
from cpqa.common import Settings
from cpqa.common import Keys

LOG_TAG = "InitializingScene"


class InitializingScene(SceneInterface):
    TEXT = "Initializing..."
    COLOR_TABLE_UPPER = [
        (180, 180, 180),
        (180, 180, 12),
        (13, 180, 180),
        (13, 180, 12),
        (180, 16, 180),
        (180, 15, 14),
        (15, 15, 180),
    ]
    COLOR_TABLE_MIDDLE = [
        (15, 15, 180),
        (16, 16, 16),
        (180, 16, 180),
        (16, 16, 16),
        (13, 180, 180),
        (16, 16, 16),
        (180, 180, 180),
    ]
    COLOR_TABLE_BOTTOM_LEFT = [
        (8, 29, 66),
        (235, 235, 235),
        (44, 0, 92),
        (16, 16, 16),
    ]
    COLOR_TABLE_BOTTOM_MIDDLE = [
        (7, 7, 7),
        (16, 16, 16),
        (24, 24, 24),
    ]
    COLOR_BOTTOM_RIGHT = (16, 16, 16)

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

        self.__screen_width = self.__settings.get(Keys.WINDOW_WIDTH)
        self.__screen_height = self.__settings.get(Keys.WINDOW_HEIGHT)
        self.__font_size = Painter.get_ajusted_font_size(
            InitializingScene.TEXT, self.__screen_width, self.__screen_height
        )
        self.__text_y_pos = (self.__screen_height - self.__font_size) // 2
        bar_upper_width = self.__screen_width / len(InitializingScene.COLOR_TABLE_UPPER)
        bar_upper_height = self.__screen_height * (2 / 3)
        self.__bar_rectangle_upper_list = []
        for i in range(len(InitializingScene.COLOR_TABLE_UPPER)):
            self.__bar_rectangle_upper_list.append(
                Rectangle(i * bar_upper_width, 0, bar_upper_width, bar_upper_height)
            )
        bar_middle_width = self.__screen_width / len(
            InitializingScene.COLOR_TABLE_MIDDLE
        )
        bar_middle_height = self.__screen_height * (1 / 12)
        self.__bar_rectangle_middle_list = []
        for i in range(len(InitializingScene.COLOR_TABLE_MIDDLE)):
            self.__bar_rectangle_middle_list.append(
                Rectangle(
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
                Rectangle(
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
                Rectangle(
                    i * bar_bottom_middle_width + (self.__screen_width * (5 / 7)),
                    bar_upper_height + bar_middle_height,
                    bar_bottom_middle_width,
                    bar_bottom_middle_height,
                )
            )
        self.__bar_rectangle_bottom_right = Rectangle(
            self.__screen_width - bar_upper_width,
            bar_upper_height + bar_middle_height,
            bar_upper_width,
            bar_bottom_middle_height,
        )

    def update(self, mut_client):
        pass

    def draw(self, canvas):
        Painter.clear(canvas)
        # draw SMPTE color bars
        for rects, colors in [
            (self.__bar_rectangle_upper_list, InitializingScene.COLOR_TABLE_UPPER),
            (self.__bar_rectangle_middle_list, InitializingScene.COLOR_TABLE_MIDDLE),
            (
                self.__bar_rectangle_bottom_left_list,
                InitializingScene.COLOR_TABLE_BOTTOM_LEFT,
            ),
            (
                self.__bar_rectangle_bottom_middle_list,
                InitializingScene.COLOR_TABLE_BOTTOM_MIDDLE,
            ),
        ]:
            for i, rect in enumerate(rects):
                Painter.fill_rect(canvas, rect, colors[i])

        Painter.fill_rect(
            canvas,
            self.__bar_rectangle_bottom_right,
            InitializingScene.COLOR_BOTTOM_RIGHT,
        )

        # Draw text
        Painter.draw_text(
            canvas,
            InitializingScene.TEXT,
            0,
            self.__text_y_pos,
            self.__font_size,
            (255, 255, 255),
        )

    def change_scene_if_needed(self, mut_client):
        if self.__is_opened:
            return MainScene
        return None

    def on_enter(self, mut_client):
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
