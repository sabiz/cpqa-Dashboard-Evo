from cpqa.mut.request import MutRequest


class EgrTemperature(MutRequest):
    @property
    def name(self):
        return "EgrTemperature"

    @property
    def name_short(self):
        return "EgrTemp"

    @property
    def request_id(self):
        return 0x12

    @property
    def unit(self):
        return "C"

    @property
    def max(self):
        return 300

    @property
    def min(self):
        return 0

    def convert(self, x):
        return (-2.7 * x + 597.7) - 32 * 5 / 9
