from cpqa.mut.request import MutRequest


class KnockVoltage(MutRequest):
    @property
    def name(self):
        return "KnockVoltage"

    @property
    def name_short(self):
        return "Knock"

    @property
    def request_id(self):
        return 0x30

    @property
    def unit(self):
        return "V"

    @property
    def max(self):
        return 50

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 0.0195 * x
