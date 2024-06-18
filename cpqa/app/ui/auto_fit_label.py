from kivy.core.text.markup import MarkupLabel
from kivy.uix.label import Label


class AutoFitLabel(Label):
    markup = True

    def on_text(self, *args, **kwargs):
        self.fit_font_size()

    def on_size(self, *args, **kwargs):
        self.fit_font_size()

    def fit_font_size(self):
        font_size = self.font_size
        while True:
            lbl = MarkupLabel(font_name=self.font_name,
                              font_size=font_size, text=self.text)
            lbl.refresh()
            lbl_available_height = (
                self.height - (self.padding[0] + self.padding[2]))
            lbl_available_width = (
                self.width - (self.padding[1] + self.padding[3]))
            if font_size > lbl_available_height:
                font_size = lbl_available_height
            elif (lbl.content_width > lbl_available_width or
                  lbl.content_height > lbl_available_height):
                font_size *= 0.99
            else:
                break

        while True:
            lbl = MarkupLabel(font_name=self.font_name,
                              font_size=font_size, text=self.text)
            lbl.refresh()
            if (lbl.content_width * 1.1 < lbl_available_width and
               lbl.content_height * 1.1 < lbl_available_height):
                font_size *= 1.1
            else:
                break
        self.font_size = font_size
