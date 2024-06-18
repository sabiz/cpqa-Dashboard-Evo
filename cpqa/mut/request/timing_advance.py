from cpqa.mut.request import MutRequest


class TimingAdvance(MutRequest):
    @property
    def name(self):
        return "TimingAdvance"

    @property
    def name_short(self):
        return "TimingAdv"

    @property
    def request_id(self):
        return 0x06

    @property
    def unit(self):
        return "deg"

    @property
    def max(self):
        return 50

    @property
    def min(self):
        return 0

    def convert(self, x):
        return x - 20
