import cv2
from cpqa.app.core import Screen
from cpqa.app.core import MouseEvents
from cpqa.common import Keys


def test_screen(mocker):
    class MockSettings:
        def get(self, x):
            if x == Keys.WINDOW_WIDTH:
                return 320
            elif x == Keys.WINDOW_HEIGHT:
                return 240
            elif x == Keys.USE_FRAME_BUFFER:
                return False

    mocker.patch("cpqa.app.core._screen.Settings", MockSettings)

    screen = Screen()
    assert screen.update(lambda canvas: None) == False
    assert screen.get_mouse_event() == []
    screen._Screen__on_mouse_event(cv2.EVENT_LBUTTONDOWN, 10, 10, 0, None)
    screen._Screen__on_mouse_event(cv2.EVENT_LBUTTONUP, 10, 10, 0, None)
    screen._Screen__on_mouse_event(cv2.EVENT_RBUTTONDOWN, 10, 10, 0, None)
    screen._Screen__on_mouse_event(cv2.EVENT_RBUTTONUP, 10, 10, 0, None)
    screen._Screen__on_mouse_event(cv2.EVENT_MBUTTONDOWN, 10, 10, 0, None)
    screen._Screen__on_mouse_event(cv2.EVENT_MBUTTONUP, 10, 10, 0, None)
    events = screen.get_mouse_event()
    assert len(events) == 6
    assert (
        events[0].event == MouseEvents.LEFT_BUTTON_DOWN
        and events[0].x == 10
        and events[0].y == 10
    )
    assert (
        events[1].event == MouseEvents.LEFT_BUTTON_UP
        and events[0].x == 10
        and events[0].y == 10
    )
    assert (
        events[2].event == MouseEvents.RIGHT_BUTTON_DOWN
        and events[0].x == 10
        and events[0].y == 10
    )
    assert (
        events[3].event == MouseEvents.RIGHT_BUTTON_UP
        and events[0].x == 10
        and events[0].y == 10
    )
    assert (
        events[4].event == MouseEvents.MIDDLE_BUTTON_DOWN
        and events[0].x == 10
        and events[0].y == 10
    )
    assert (
        events[5].event == MouseEvents.MIDDLE_BUTTON_UP
        and events[0].x == 10
        and events[0].y == 10
    )
    assert screen.get_mouse_event() == []
    screen._Screen__destry()
    screen._Screen__destry()
    assert screen.update(lambda canvas: None) == True
