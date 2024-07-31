import atexit
import cv2
import numpy as np
from queue import Queue
from cpqa.common import Settings
from cpqa.common import Keys
from collections import namedtuple
from enum import Enum
from enum import auto

MouseEvent = namedtuple("MouseEvent", ("event", "x", "y"))


class MouseEvents(Enum):
    LEFT_BUTTON_DOWN = auto()
    LEFT_BUTTON_UP = auto()
    RIGHT_BUTTON_DOWN = auto()
    RIGHT_BUTTON_UP = auto()
    MIDDLE_BUTTON_DOWN = auto()
    MIDDLE_BUTTON_UP = auto()


class Screen:
    __instance = None
    __WINDOW_NAME = "Cpqa-Dashboard-Evo"

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Screen, cls).__new__(cls)
        return cls.__instance

    def __init__(self):
        settings = Settings()
        width = settings.get(Keys.WINDOW_WIDTH)
        height = settings.get(Keys.WINDOW_HEIGHT)
        self.__mouse_event_queue = Queue()

        self.__canvas = np.zeros((height, width, 3), np.uint8)
        self.__use_frame_buffer = settings.get(Keys.USE_FRAME_BUFFER)
        self.__destryed = False
        atexit.register(self.__destry)

        cv2.imshow(Screen.__WINDOW_NAME, self.__canvas)
        if not self.__use_frame_buffer:
            cv2.setMouseCallback(Screen.__WINDOW_NAME, self.__on_mouse_event)

    def update(self, draw_func):
        if self.__destryed:
            return True
        result = False
        if self.__use_frame_buffer:
            result = self.__update_for_frame_buffer(draw_func)
        else:
            result = self.__update_window(draw_func)

        if result:
            self.__destry()
        return result

    def get_mouse_event(self):
        result = []
        while not self.__mouse_event_queue.empty():
            result.append(self.__mouse_event_queue.get())
        return result

    def __update_window(self, draw_func):
        if cv2.getWindowProperty(Screen.__WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            return True
        draw_func(self.__canvas)
        cv2.imshow(Screen.__WINDOW_NAME, self.__canvas)
        cv2.waitKey(1)
        return False

    def __update_for_frame_buffer(self, draw_func):
        draw_func(self.__canvas)
        raise NotImplementedError("Frame buffer is not implemented yet")
        # TODO

    def __on_mouse_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            return
        converted_event = None
        if event == cv2.EVENT_LBUTTONDOWN:
            converted_event = MouseEvents.LEFT_BUTTON_DOWN
        elif event == cv2.EVENT_LBUTTONUP:
            converted_event = MouseEvents.LEFT_BUTTON_UP
        elif event == cv2.EVENT_RBUTTONDOWN:
            converted_event = MouseEvents.RIGHT_BUTTON_DOWN
        elif event == cv2.EVENT_RBUTTONUP:
            converted_event = MouseEvents.RIGHT_BUTTON_UP
        elif event == cv2.EVENT_MBUTTONDOWN:
            converted_event = MouseEvents.MIDDLE_BUTTON_DOWN
        elif event == cv2.EVENT_MBUTTONUP:
            converted_event = MouseEvents.MIDDLE_BUTTON_UP
        self.__mouse_event_queue.put(MouseEvent(converted_event, x, y))

    def __destry(self):
        if self.__destryed:
            return
        self.__destryed = True
        if self.__use_frame_buffer:
            raise NotImplementedError("Frame buffer is not implemented yet")
            # TODO
        else:
            cv2.destroyAllWindows()
