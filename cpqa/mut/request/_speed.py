from cpqa.mut.request import MutRequest


class Speed(MutRequest):
    @property
    def name(self):
        return "Speed"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x2F

    @property
    def unit(self):
        return "km/h"

    @property
    def max(self):
        return 280

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 2 * x
