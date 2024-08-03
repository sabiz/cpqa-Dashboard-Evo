from cpqa.app.scene._exit_scene import ExitScene


def test_exit_scene(mocker):
    exit_scene = ExitScene()

    exit_mock = mocker.patch("sys.exit")
    exit_scene.on_enter(None)
    exit_mock.assert_called_once()

    exit_scene.update(None)
    assert True

    mocker.patch("cpqa.app.scene._exit_scene.Painter")
    exit_scene.draw(None)
    assert True

    exit_scene.change_scene_if_needed(None)
    assert True

    exit_scene.on_exit(None)
    assert True
