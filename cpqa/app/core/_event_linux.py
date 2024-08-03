import cv2
import evdev


class EventLinux:
    def __init__(self, event_path):
        self.__input_device = evdev.InputDevice(event_path)
        self.__last_position = (0, 0)

    def close(self):
        self.__input_device.close()

    def read_mouse_event(self, event_callback):
        try:
            for event in self.__input_device.read():
                if event.type == evdev.ecodes.EV_ABS:
                    if event.code == evdev.ecodes.ABS_X:
                        self.__last_position = (
                            event.value,
                            self.__last_position[1],
                        )
                    elif event.code == evdev.ecodes.ABS_Y:
                        self.__last_position = (
                            self.__last_position[0],
                            event.value,
                        )
                elif event.type == evdev.ecodes.EV_KEY:
                    ev_code = None
                    if event.code == evdev.ecodes.BTN_TOUCH:
                        if event.value == 1:
                            ev_code = cv2.EVENT_LBUTTONDOWN
                        else:
                            ev_code = cv2.EVENT_LBUTTONUP
                    if ev_code is not None:
                        event_callback(
                            ev_code,
                            self.__last_position[0],
                            self.__last_position[1],
                            0,
                            None,
                        )
        except BlockingIOError:
            pass
