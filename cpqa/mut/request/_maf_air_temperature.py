from cpqa.mut.request import MutRequest


class MafAirTemperature(MutRequest):
    @property
    def name(self):
        return "MafAirTemperature"

    @property
    def name_short(self):
        return "MafAirTemp"

    @property
    def request_id(self):
        return 0x11

    @property
    def unit(self):
        return "C"

    @property
    def max(self):
        return 260

    @property
    def min(self):
        return -40

    def convert(self, x):
        return x - 40
