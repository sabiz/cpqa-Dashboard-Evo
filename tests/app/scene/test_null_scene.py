from cpqa.app.scene._null_scene import NullScene
from cpqa.app.scene._initializing_scene import InitializingScene


def test_null_scene(mocker):
    null_scene = NullScene()
    null_scene.on_enter(None)
    null_scene.update(None)
    mocker.patch("cpqa.app.scene._null_scene.Painter")
    null_scene.draw(None)
    assert null_scene.change_scene_if_needed(None) == InitializingScene

    null_scene.on_exit(None)
