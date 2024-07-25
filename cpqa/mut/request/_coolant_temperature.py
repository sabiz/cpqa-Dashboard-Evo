from cpqa.mut.request import MutRequest


class CoolantTemperature(MutRequest):
    @property
    def name(self):
        return "CoolantTemperature"

    @property
    def name_short(self):
        return "CoolantTemp"

    @property
    def request_id(self):
        return 0x10

    @property
    def unit(self):
        return "C"

    @property
    def max(self):
        # Normal 85-95
        return 190

    @property
    def min(self):
        return 0

    def convert(self, x):
        return x - 40
