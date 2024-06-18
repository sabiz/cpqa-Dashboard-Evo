from cpqa.app.ui.auto_fit_label import AutoFitLabel


class ValueNameLabel(AutoFitLabel):

    __on_tap_func = None

    def on_touch_up(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if self.__on_tap_func is None:
            return
        self.__on_tap_func(touch)

    def set_on_tap_func(self, func):
        self.__on_tap_func = func
