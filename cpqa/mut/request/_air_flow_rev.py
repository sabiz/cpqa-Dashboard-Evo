from cpqa.mut.request import MutRequest


class AirFlowRev(MutRequest):
    @property
    def name(self):
        return "AirFlowRev"

    @property
    def name_short(self):
        return "AccelEnrich"

    @property
    def request_id(self):
        return 0x1D

    @property
    def unit(self):
        return "load"

    @property
    def max(self):
        return 300

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 200 * x / 255
