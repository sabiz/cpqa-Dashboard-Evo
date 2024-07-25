from cpqa.mut.request import MutRequest


class AirVolume(MutRequest):
    @property
    def name(self):
        return "AirVolume"

    @property
    def name_short(self):
        return "AirVol"

    @property
    def request_id(self):
        return 0x2C

    @property
    def unit(self):
        return " "

    @property
    def max(self):
        return 255

    @property
    def min(self):
        return 0

    def convert(self, x):
        return x
