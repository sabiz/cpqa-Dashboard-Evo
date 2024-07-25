from cpqa.mut.request import MutRequest


class KnockSum(MutRequest):
    @property
    def name(self):
        return "KnockSum"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x26

    @property
    def unit(self):
        return "count"

    @property
    def max(self):
        return 50

    @property
    def min(self):
        return 0

    def convert(self, x):
        return x
