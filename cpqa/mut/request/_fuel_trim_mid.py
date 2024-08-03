from cpqa.mut.request import MutRequest


class FuelTrimMid(MutRequest):
    @property
    def name(self):
        return "FuelTrimMid"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x0D

    @property
    def unit(self):
        return "%"

    @property
    def max(self):
        return 15

    @property
    def min(self):
        return -15

    def convert(self, x):
        return (0.1961 * x) - 25  # 0.78125 * x ??
