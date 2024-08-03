import time
from cpqa.app.core import Scheduler
from cpqa.app.scene._initializing_scene import InitializingScene
from cpqa.app.scene._main_scene import MainScene
from cpqa.common import Keys
from cpqa.mut import MutResult


def test_initializing_scene(mocker):
    class MockSettings:
        def get(self, x):
            if x == Keys.DEVICE_INDEX:
                return 1
            elif x == Keys.WINDOW_WIDTH:
                return 320
            elif x == Keys.WINDOW_HEIGHT:
                return 240

    mocker.patch("cpqa.app.scene._initializing_scene.Painter")
    mocker.patch(
        "cpqa.app.scene._initializing_scene.Settings.get",
        side_effect=MockSettings().get,
    )

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

    initializing_scene.on_enter(mockMutClient)
    scheduler.tick()
    result = initializing_scene.change_scene_if_needed(mockMutClient)
    assert result is None

    time.sleep(1)
    scheduler.tick()
    assert mockMutClient.is_opened == True

    initializing_scene.update(mockMutClient)

    initializing_scene.draw(None)

    result = initializing_scene.change_scene_if_needed(mockMutClient)
    assert result == MainScene

    initializing_scene.on_exit(None)
