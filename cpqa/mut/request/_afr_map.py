from cpqa.mut.request import MutRequest


class AfrMap(MutRequest):
    @property
    def name(self):
        return "AfrMap"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x32

    @property
    def unit(self):
        return "AFR"

    @property
    def max(self):
        return 255

    @property
    def min(self):
        return 0

    def convert(self, x):
        return (14.7 * 128.0) / (x + 0.000000000001)
