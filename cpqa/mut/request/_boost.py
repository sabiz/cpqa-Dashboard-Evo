from cpqa.mut.request import MutRequest


class Boost(MutRequest):
    @property
    def name(self):
        return "Boost"

    @property
    def name_short(self):
        return "MAP"

    @property
    def request_id(self):
        return 0x38

    @property
    def unit(self):
        return "kgf/cm2"

    @property
    def max(self):
        return 350

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 0.01334 * x
