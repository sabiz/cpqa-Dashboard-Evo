import time
from cpqa.app.core import Scheduler
from cpqa.app.scene._initializing_scene import InitializingScene
from cpqa.app.scene._main_scene import MainScene
from cpqa.common import Keys
from cpqa.mut import MutResult


def test_initializing_scene(mocker):
    mocker.patch("pyray.get_screen_width", return_value=320)
    mocker.patch("pyray.get_screen_height", return_value=240)
    mocker.patch(
        "cpqa.app.scene._initializing_scene.get_ajusted_font_size", return_value=10
    )  # from cpqa.app.util.graphics_util import get_ajusted_font_size

    class MockSettings:
        def get(self, x):
            if x == Keys.DEVICE_INDEX:
                return 1

    class MockMutClient:
        def __init__(self):
            self.is_opened = False

        def exist_device(self):
            return True

        def open(self, index):
            self.is_opened = True
            return MutResult(0, "OK", True)

    scheduler = Scheduler()
    mockMutClient = MockMutClient()
    initializing_scene = InitializingScene()
    mocker.patch.object(
        initializing_scene, "_InitializingScene__settings", MockSettings()
    )

    initializing_scene.on_enter(mockMutClient)
    scheduler.tick()
    result = initializing_scene.change_scene_if_needed(mockMutClient)
    assert result is None

    time.sleep(1)
    scheduler.tick()
    assert mockMutClient.is_opened == True

    initializing_scene.update(mockMutClient)

    pr_cler_background = mocker.patch("pyray.clear_background")
    mocker.patch("pyray.draw_text")
    mocker.patch("pyray.draw_rectangle_pro")
    initializing_scene.draw()
    pr_cler_background.assert_called_once()

    result = initializing_scene.change_scene_if_needed(mockMutClient)
    assert result == MainScene

    initializing_scene.on_exit(None)
