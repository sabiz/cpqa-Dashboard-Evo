import numpy as np
from cpqa.app.core import Painter
from cpqa.app.core import Rectangle
from cpqa.app.core import Point


def test_painter_clear(mocker):
    canvas = np.full((100, 100, 3), 1)
    Painter.clear(canvas)
    assert np.all(canvas == np.zeros((100, 100, 3), np.uint8))


def test_painter_fill_rect(mocker):
    canvas = np.full((100, 100, 3), 1)
    Painter.fill_rect(canvas, Rectangle(10, 10, 20, 20), (255, 0, 0))
    assert np.all(canvas[10:30, 10:30] == np.full((20, 20, 3), (0, 0, 255)))  # BGR


def test_painter_draw_ring(mocker):
    canvas = np.full((100, 100, 3), 1)
    Painter.draw_ring(canvas, Point(50, 50), 50, (255, 0, 0), 3)
    assert canvas[50, 50].tolist() == [1, 1, 1]  # BGR
    assert canvas[99, 50].tolist() == [0, 0, 255]  # BGR


def test_painter_draw_line(mocker):
    canvas = np.full((100, 100, 3), 1)
    Painter.draw_line(canvas, Point(0, 0), Point(50, 50), (255, 0, 0), 3)
    assert canvas[0, 0].tolist() == [0, 0, 255]  # BGR
    assert canvas[50, 50].tolist() == [0, 0, 255]  # BGR
    assert canvas[99, 99].tolist() == [1, 1, 1]  # BGR


def test_painter_get_ajusted_font_size(mocker):
    assert Painter.get_ajusted_font_size("", 100, 100) == 1
    assert Painter.get_ajusted_font_size("a", 100, 100) == 5


def test_painter_draw_text(mocker):
    canvas = np.full((50, 50, 3), 1)
    Painter.draw_text(canvas, "I", 0, 25, 2, (255, 0, 0))
    assert canvas[10, 10].tolist() == [255, 0, 0]  # BGR
    assert canvas[0, 0].tolist() == [1, 1, 1]  # BGR
