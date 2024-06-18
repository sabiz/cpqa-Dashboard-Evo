from cpqa.mut.request import MutRequest


class AirTemperature(MutRequest):
    @property
    def name(self):
        return "AirTemperature"

    @property
    def name_short(self):
        return "AirTemp"

    @property
    def request_id(self):
        return 0x3A

    @property
    def unit(self):
        return "C"

    @property
    def max(self):
        return 190

    @property
    def min(self):
        return 0

    def convert(self, x):
        return x
