from cpqa.mut.request import MutRequest


class ThrottlePosition(MutRequest):
    @property
    def name(self):
        return "ThrottlePosition"

    @property
    def name_short(self):
        return "TPS"

    @property
    def request_id(self):
        return 0x17

    @property
    def unit(self):
        return "%"

    @property
    def max(self):
        return 100

    @property
    def min(self):
        return 0

    def convert(self, x):
        return x * 100 / 255
