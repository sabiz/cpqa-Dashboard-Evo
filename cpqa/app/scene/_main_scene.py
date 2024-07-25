import pyray as pr
import subprocess
from collections import namedtuple
from ._scene_interface import SceneInterface
from ._exit_scene import ExitScene
from cpqa.app.core import Scheduler
from cpqa.common import Settings
from cpqa.common import Keys
from cpqa.common import log_d
from cpqa.common import log_e
from cpqa.app.util.graphics_util import Rectangle
from cpqa.app.util.graphics_util import Point
from cpqa.app.util.graphics_util import get_ajusted_font_size
from cpqa.app.util.graphics_util import get_text_width
from cpqa.mut import MutClient

RequestJob = namedtuple("RequestJob", ("request", "interval"))

LOG_TAG = "MainScene"


class MainScene(SceneInterface):
    COLOR_LABEL_BG = pr.Color(169, 29, 58, 255)
    COLOR_LABEL_TEXT = pr.Color(255, 230, 230, 255)
    COLOR_POWER_BG = pr.Color(0, 0, 0, 255)
    COLOR_POWER_LINE = pr.Color(169, 29, 58, 255)

    def __init__(self):
        self.__scheduler = Scheduler()
        self.__screen_width = None
        self.__screen_height = None
        self.__label_area = None
        self.__label_font_size = 1
        self.__value_area = None
        self.__value_font_size = 1
        self.__unit_area = None
        self.__unit_font_size = 1
        self.__power_point = None
        self.__power_radius = None

        self.__label_text = ""
        self.__last_label_text = ""
        self.__value_text = ""
        self.__unit_text = ""
        self.__last_unit_text = ""

        self.__request_table = []
        self.__current_request_index = 0
        self.__scheduled_task_id = None
        self.__is_closed = False

    def update(self, mut_client):
        if pr.is_mouse_button_released(pr.MOUSE_LEFT_BUTTON) and not self.__is_closed:
            p = pr.get_mouse_position()
            if (
                self.__label_area.x
                <= p.x
                <= self.__label_area.x + self.__label_area.width
                and self.__label_area.y
                <= p.y
                <= self.__label_area.y + self.__label_area.height
            ):
                self.__change_request(mut_client)

            elif self.__power_point.x - (
                self.__power_radius * 2
            ) <= p.x <= self.__power_point.x + (
                self.__power_radius * 2
            ) and self.__power_point.y - (
                self.__power_radius * 2
            ) <= p.y <= self.__power_point.y + (self.__power_radius * 2):
                self.__push_power(mut_client)

    def draw(self):
        pr.clear_background(pr.BLACK)
        # draw label ----------------------------
        pr.draw_rectangle(
            0,
            self.__label_area.y,
            self.__label_area.width,
            self.__label_area.height,
            MainScene.COLOR_LABEL_BG,
        )
        pr.draw_text(
            self.__label_text,
            self.__label_area.x,
            self.__label_area.y,
            self.__label_font_size,
            MainScene.COLOR_LABEL_TEXT,
        )

        # draw value ----------------------------
        pr.draw_text(
            self.__value_text,
            self.__value_area.x,
            self.__value_area.y,
            self.__value_font_size,
            pr.WHITE,
        )

        # draw unit ----------------------------
        pr.draw_text(
            self.__unit_text,
            self.__unit_area.x,
            self.__value_area.y + self.__value_font_size,
            self.__unit_font_size,
            pr.WHITE,
        )

        # draw power ----------------------------
        pr.draw_ring(
            pr.Vector2(self.__power_point.x, self.__power_point.y),
            self.__power_radius,
            self.__power_radius - 5,
            0,
            360,
            1,
            MainScene.COLOR_POWER_LINE,
        )
        pr.draw_line_ex(
            pr.Vector2(
                self.__power_point.x,
                0,
            ),
            pr.Vector2(
                self.__power_point.x,
                self.__power_radius,
            ),
            9,
            MainScene.COLOR_POWER_BG,
        )
        pr.draw_line_ex(
            pr.Vector2(
                self.__power_point.x,
                0,
            ),
            pr.Vector2(
                self.__power_point.x,
                self.__power_radius,
            ),
            5,
            MainScene.COLOR_POWER_LINE,
        )

    def change_scene_if_needed(self, mut_client):
        if self.__is_closed:
            return ExitScene
        return None

    def on_enter(self, mut_client):
        if self.__screen_width is None or self.__screen_height is None:
            self.__screen_width = pr.get_screen_width()
            self.__screen_height = pr.get_screen_height()
            self.__label_area = Rectangle(
                0,
                int(self.__screen_height * 0.8),
                self.__screen_width,
                int(self.__screen_height * 0.2),
            )
            self.__power_radius = int(self.__screen_width * 0.05)
            self.__power_point = Point(
                int(self.__screen_width - (self.__power_radius * 1.2)),
                int(self.__power_radius * 1.2),
            )
            self.__value_area = Rectangle(
                10,
                int(self.__screen_height * 0.2),
                int(self.__screen_width * 0.8),
                int(self.__screen_height * 0.4),
            )
            self.__unit_area = Rectangle(
                int(self.__screen_width * 0.8),
                0,
                int(self.__screen_width * 0.2),
                int(self.__screen_height * 0.2),
            )

        self.__load_request_settings()
        self.__start_request(mut_client)

    def on_exit(self, mut_client):
        if self.__scheduled_task_id is not None:
            self.__scheduler.remove(self.__scheduled_task_id)

    def __load_request_settings(self):
        self.__request_table.clear()
        settings = Settings()
        for key in Settings.REQUEST_KEY_LIST:
            request = settings.get(key)
            if not request.enabled:
                continue
            self.__request_table.append(
                RequestJob(
                    MutClient.settings_key_to_request_instance(key), request.interval
                )
            )
        log_d(LOG_TAG, f"request_table: {self.__request_table}")

    def __start_request(self, mut_client):
        self.__scheduled_task_id = self.__scheduler.add_interval(
            self.__run_mut_request(
                self.__request_table[self.__current_request_index].request, mut_client
            ),
            self.__request_table[self.__current_request_index].interval,
        )

    def __run_mut_request(self, request, mut_client):
        def run_mut_request_impl():
            log_d(LOG_TAG, "Process MUT Request")
            val = mut_client.request(request)
            self.__update_value(request, val)

        return run_mut_request_impl

    def __update_value(self, request, value):
        if value is None:
            self.__value_text = "N/A"
            self.__unit_text = ""
            self.__label_text = "Connection lost"
        elif isinstance(value, str):
            self.__value_text = value
            self.__unit_text = ""
            self.__label_text = request.name
        else:
            self.__value_text = str(round(value, 2))
            self.__unit_text = request.unit
            self.__label_text = request.name

        # update font size
        if self.__last_label_text != self.__label_text:
            self.__last_label_text = self.__label_text
            self.__label_font_size = get_ajusted_font_size(
                self.__label_text, self.__label_area.width - 10
            )
            if self.__label_area.height < self.__label_font_size:
                self.__label_font_size = self.__label_area.height
            self.__label_area.x = int(
                (
                    self.__label_area.width
                    - get_text_width(self.__label_text, self.__label_font_size)
                )
                // 2
            )

        self.__value_font_size = get_ajusted_font_size(
            self.__value_text, self.__value_area.width
        )
        if self.__value_area.height < self.__value_font_size:
            self.__value_font_size = self.__value_area.height
        self.__value_area.x = int(
            (
                self.__value_area.width
                - get_text_width(self.__value_text, self.__value_font_size)
            )
            // 2
        )

        if self.__last_unit_text != self.__unit_text:
            self.__last_unit_text = self.__unit_text
            self.__unit_font_size = get_ajusted_font_size(
                self.__unit_text, self.__unit_area.width
            )
            if self.__unit_area.height < self.__unit_font_size:
                self.__unit_font_size = self.__unit_area.height
            self.__unit_area.x = int(
                self.__value_area.width
                + (
                    self.__unit_area.width
                    - get_text_width(self.__unit_text, self.__unit_font_size)
                )
                // 2
            )

    def __change_request(self, mut_client):
        log_d(LOG_TAG, "Change Request")
        self.__scheduler.remove_interval(self.__scheduled_task_id)
        self.__scheduled_task_id = None
        self.__current_request_index = (self.__current_request_index + 1) % len(
            self.__request_table
        )
        self.__start_request(mut_client)

    def __push_power(self, mut_client):
        self.__scheduler.remove_interval(self.__scheduled_task_id)
        self.__scheduled_task_id = None
        mut_client.close()

        settings = Settings()
        cmd = settings.get(Keys.POWER_BUTTON_COMMAND)
        log_d(LOG_TAG, f"Power Button Command: {cmd}")
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, check=True)
            log_d(LOG_TAG, f"Power Button Command Result: {result.stdout}")
            self.__is_closed = True
        except subprocess.CalledProcessError as e:
            log_e(LOG_TAG, f"Power Button Command Error: {e}")
            raise e
