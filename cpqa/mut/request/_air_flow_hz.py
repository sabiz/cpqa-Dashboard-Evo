from cpqa.mut.request import MutRequest


class AirFlowHz(MutRequest):
    @property
    def name(self):
        return "AirFlowHz"

    @property
    def name_short(self):
        return "AirFlow"

    @property
    def request_id(self):
        return 0x1A

    @property
    def unit(self):
        return "Hz"

    @property
    def max(self):
        return 1650

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 6.25 * x
