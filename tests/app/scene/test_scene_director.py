from cpqa.app.scene import SceneDirector
from cpqa.app.scene._null_scene import NullScene


def test_scene_director(mocker):
    scene_director = SceneDirector()

    class MockScene:
        def __init__(self):
            self.update_called = False
            self.draw_called = False
            self.change_scene_if_needed_called = False
            self.on_enter_called = False
            self.on_exit_called = False

        def update(self, mut_client):
            self.update_called = True

        def draw(self):
            self.draw_called = True

        def change_scene_if_needed(self, mut_client):
            if not self.change_scene_if_needed_called:
                self.change_scene_if_needed_called = True
                return None
            return "MOCK2"

        def on_enter(self, mut_client):
            self.on_enter_called = True

        def on_exit(self, mut_client):
            self.on_exit_called = True

    mocker.patch.object(scene_director, "_SceneDirector__scene", MockScene)
    mock_scene = MockScene()
    mock_scene2 = MockScene()
    scene_director._SceneDirector__scene_dict.update(
        {MockScene: mock_scene, "MOCK2": mock_scene2}
    )
    scene_director.update(None)
    assert mock_scene.update_called == True

    pr_begin_drawing = mocker.patch("pyray.begin_drawing")
    pr_end_drawing = mocker.patch("pyray.end_drawing")
    mocker.patch("pyray.draw_fps")
    scene_director.draw()
    pr_begin_drawing.assert_called_once()
    pr_end_drawing.assert_called_once()
    assert mock_scene.draw_called == True

    scene_director.change_scene_if_needed(None)
    scene_director.change_scene_if_needed(None)
    assert mock_scene.change_scene_if_needed_called == True
    assert mock_scene.on_exit_called == True
    assert mock_scene2.on_enter_called == True
