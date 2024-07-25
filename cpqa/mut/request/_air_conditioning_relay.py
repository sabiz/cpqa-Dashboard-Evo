from cpqa.mut.request import MutRequest


class AirConditioningRelay(MutRequest):
    @property
    def name(self):
        return "AirConditioningRelay"

    @property
    def name_short(self):
        return "ACRelaySw"

    @property
    def request_id(self):
        return 0x49

    @property
    def unit(self):
        return "ON/OFF"

    @property
    def max(self):
        return 255

    @property
    def min(self):
        return 0

    def convert(self, x):
        return x & 0b0000_0100
