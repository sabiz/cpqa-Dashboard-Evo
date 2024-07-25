from cpqa.mut.request import MutRequest


class Barometer(MutRequest):
    @property
    def name(self):
        return "Barometer"

    @property
    def name_short(self):
        return "Baro"

    @property
    def request_id(self):
        return 0x15

    @property
    def unit(self):
        return "kPa"

    @property
    def max(self):
        return 126

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 0.49 * x
