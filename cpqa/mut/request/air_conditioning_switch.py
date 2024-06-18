from cpqa.mut.request import MutRequest


class AirConditioningSwitch(MutRequest):
    @property
    def name(self):
        return "AirConditioningSwitch"

    @property
    def name_short(self):
        return "ACSwitch"

    @property
    def request_id(self):
        return 0x4A

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
        return x & 0b0001_0000
