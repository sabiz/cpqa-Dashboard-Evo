import pyray as pr
import colorsys
from collections import namedtuple
from dataclasses import dataclass

COLOR_TRANSPARENT = pr.Color(0, 0, 0, 0)

Point = namedtuple("Point", ("x", "y"))


@dataclass
class Rectangle:
    x: int
    y: int
    width: int
    height: int


def get_ajusted_font_size(text, width):
    if len(text) == 0:
        return 1
    font = pr.get_font_default()
    length = pr.text_length(text)
    font_size = 1
    while True:
        text_width = __get_text_width(text, font_size, font, length)
        if text_width < width // 2:
            font_size += 10
        elif text_width < width:
            font_size += 1
        elif text_width >= width - 10:
            break
    return font_size


def get_text_width(text, font_size):
    if len(text) == 0:
        return 0
    font = pr.get_font_default()
    length = pr.text_length(text)
    return __get_text_width(text, font_size, font, length)


def __get_text_width(text, font_size, font, length):
    if len(text) == 0:
        return 0
    scale_factor = font_size / font.baseSize
    i = 0
    text_width = 0
    while i < length:
        code_point_byte_count = pr.ffi.new("int *", 1)
        code_point = pr.get_codepoint(text[i], code_point_byte_count)
        index = pr.get_glyph_index(font, code_point)
        if code_point == 0x3F:
            code_point_byte_count[0] = 1
        i += code_point_byte_count[0] - 1
        glyph_width = (
            font.recs[index].width * scale_factor
            if font.glyphs[index].advanceX == 0
            else font.glyphs[index].advanceX * scale_factor
        )
        if i + 1 < length:
            glyph_width += font_size * 0.1
        text_width += glyph_width
        i += 1
        pr.ffi.release(code_point_byte_count)
    return text_width


def hsv_to_color(h, s, v):
    rgb = colorsys.hsv_to_rgb(h, s, v)
    return pr.Color(int(rgb[0] * 255), int(rgb[1] * 255), int(rgb[2] * 255), 255)
