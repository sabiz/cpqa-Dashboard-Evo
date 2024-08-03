import time
import subprocess
from cpqa.app.core import Scheduler
from cpqa.app.core import MouseEvent
from cpqa.app.core import MouseEvents
from cpqa.app.scene._main_scene import MainScene
from cpqa.app.scene._exit_scene import ExitScene
from cpqa.common import Keys
from cpqa.common._settings import RequestSetting


def test_main_scene(mocker):
    class MockSettings:
        REQUEST_KEY_LIST = [
            Keys.REQUEST_BOOST,
            Keys.REQUEST_SPEED,
            Keys.REQUEST_ENGINE_RPM,
        ]

        def get(self, x):
            if x == Keys.REQUEST_BOOST:
                return RequestSetting(True, 100)
            elif x == Keys.REQUEST_SPEED:
                return RequestSetting(True, 100)
            elif x == Keys.REQUEST_ENGINE_RPM:
                return RequestSetting(False, 100)
            elif x == Keys.POWER_BUTTON_COMMAND:
                return "cmd"
            elif x == Keys.WINDOW_WIDTH:
                return 320
            elif x == Keys.WINDOW_HEIGHT:
                return 240

    mocker.patch("cpqa.app.scene._main_scene.Painter")
    mocker.patch(
        "cpqa.app.scene._main_scene.Settings.get",
        side_effect=MockSettings().get,
    )

    class MockMutClient:
        def __init__(self):
            self.is_closed = False
            self.count = 0

        def request(self, request):
            assert self.is_closed is False
            if self.count == 0:
                self.count += 1
                return 100.0
            elif self.count == 1:
                self.count += 1
                return "ERROR"
            else:
                self.count = 0
                return None

        def close(self):
            self.is_closed = True

    scheduler = Scheduler()
    mockMutClient = MockMutClient()
    main_scene = MainScene()
    mocker.patch("cpqa.app.scene._main_scene.Settings", MockSettings)

    main_scene.on_enter(mockMutClient)
    scheduler.tick()
    result = main_scene.change_scene_if_needed(mockMutClient)
    assert result is None
    time.sleep(1)
    scheduler.tick()
    assert mockMutClient.count == 1
    assert main_scene._MainScene__label_text == "Boost"
    assert main_scene._MainScene__value_text == "100.0"
    assert main_scene._MainScene__unit_text == "kgf/cm2"

    main_scene.update(mockMutClient)
    main_scene.draw(None)

    mocker.patch(
        "cpqa.app.scene._main_scene.Screen.get_mouse_event",
        return_value=[MouseEvent(MouseEvents.LEFT_BUTTON_UP, 120, 200)],
    )
    main_scene.update(mockMutClient)
    time.sleep(1)
    scheduler.tick()
    assert mockMutClient.count == 2
    assert main_scene._MainScene__label_text == "Speed"
    assert main_scene._MainScene__value_text == "ERROR"
    assert main_scene._MainScene__unit_text == ""
    time.sleep(1)
    scheduler.tick()
    assert mockMutClient.count == 0
    assert main_scene._MainScene__label_text == "Connection lost"
    assert main_scene._MainScene__value_text == "N/A"
    assert main_scene._MainScene__unit_text == ""

    mocker.patch(
        "cpqa.app.scene._main_scene.Screen.get_mouse_event",
        return_value=[MouseEvent(MouseEvents.LEFT_BUTTON_UP, 320, 0)],
    )

    def subprocess_run(*args, **kwargs):
        assert args[0] == "cmd"
        return subprocess.CompletedProcess("cmd", 0, "", "")

    mocker.patch("subprocess.run", side_effect=subprocess_run)
    main_scene.update(mockMutClient)
    assert mockMutClient.is_closed is True

    result = main_scene.change_scene_if_needed(mockMutClient)
    assert result == ExitScene

    main_scene.on_exit(None)
