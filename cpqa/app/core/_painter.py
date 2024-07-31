import cv2
import numpy as np
from collections import namedtuple
from dataclasses import dataclass

Point = namedtuple("Point", ("x", "y"))


@dataclass
class Rectangle:
    x: float
    y: float
    width: float
    height: float


class Painter:
    @staticmethod
    def clear(canvas):
        h, w, c = canvas.shape[:3]
        cv2.rectangle(canvas, (0, 0), (w - 1, h - 1), (0, 0, 0), -1)

    @staticmethod
    def fill_rect(canvas, rect, color):
        cv2.rectangle(
            canvas,
            (int(rect.x), int(rect.y)),
            (int(rect.x + rect.width), int(rect.y + rect.height)),
            Painter.__rgb_2_bgr(color),
            cv2.FILLED,
            cv2.LINE_AA,
        )

    @staticmethod
    def draw_ring(canvas, center, radius, color, thickness):
        cv2.circle(
            canvas,
            (int(center.x), int(center.y)),
            int(radius),
            Painter.__rgb_2_bgr(color),
            thickness,
            cv2.LINE_AA,
        )

    @staticmethod
    def draw_line(canvas, start, end, color, thickness):
        cv2.line(
            canvas,
            (int(start.x), int(start.y)),
            (int(end.x), int(end.y)),
            Painter.__rgb_2_bgr(color),
            thickness,
            cv2.LINE_AA,
        )

    @staticmethod
    def get_ajusted_font_size(text, width, height, thickness=1):
        if len(text) == 0:
            return 1
        font_size = 1
        while True:
            (w, h), baseline = cv2.getTextSize(
                text, cv2.FONT_HERSHEY_DUPLEX, font_size, thickness
            )
            if w < width and h < height:
                font_size += 1
            elif w >= width - 10 or h >= height - 10:
                break
        return font_size

    @staticmethod
    def draw_text(canvas, text, x, y, font_size, color, thickness=2):
        Painter.__draw_text(canvas, text, x, y, font_size, color, thickness)

    @staticmethod
    def draw_text_area(
        canvas, text, x, y, width, height, font_size, color, thickness=2
    ):
        Painter.__draw_text(
            canvas, text, x, y, font_size, color, thickness, width, height
        )

    @staticmethod
    def __draw_text(
        canvas, text, x, y, font_size, color, thickness=2, width=None, height=None
    ):
        mask = Painter.__create_text_mask(text, color, font_size, thickness)
        if width is None:
            width = min(mask.shape[1], canvas.shape[1] - x)
        if height is None:
            height = min(mask.shape[0], canvas.shape[0] - y)
        mask = cv2.resize(mask, (width, height))
        if color == (0, 0, 0):
            canvas[y - height : y, x : x + width, :] = np.where(
                mask[:, :, 3:] < 255,
                mask[:, :, :3],
                canvas[y - height : y, x : x + width, :],
            )
        else:
            canvas[y - height : y, x : x + width, :] = np.where(
                mask[:, :, 3:] > 0,
                mask[:, :, :3],
                canvas[y - height : y, x : x + width, :],
            )

    @staticmethod
    def __create_text_mask(text, color, font_size, thickness):
        (text_width, text_height), base_line = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_DUPLEX, font_size, thickness
        )
        text_height += base_line
        if color == (0, 0, 0):
            mask = np.full((text_height, text_width, 3), 255, dtype=np.uint8)
        else:
            mask = np.zeros((text_height, text_width, 3), dtype=np.uint8)

        cv2.putText(
            mask,
            text,
            (0, text_height - base_line),
            cv2.FONT_HERSHEY_DUPLEX,
            font_size,
            Painter.__rgb_2_bgr(color),
            thickness,
            cv2.LINE_AA,
        )
        mask = cv2.merge(
            (
                mask[:, :, 2],
                mask[:, :, 1],
                mask[:, :, 0],
                (mask[:, :, 0] + mask[:, :, 1] + mask[:, :, 2]),
            )
        )
        return mask

    @staticmethod
    def __rgb_2_bgr(color):
        return color[2], color[1], color[0]
