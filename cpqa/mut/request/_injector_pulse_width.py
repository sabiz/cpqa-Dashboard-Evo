from cpqa.mut.request import MutRequest


class InjectorPulseWidth(MutRequest):
    @property
    def name(self):
        return "InjectorPulseWidth"

    @property
    def name_short(self):
        return "InjPulseWidth"

    @property
    def request_id(self):
        return 0x29

    @property
    def unit(self):
        return "ms"

    @property
    def max(self):
        return 66

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 0.256 * x
