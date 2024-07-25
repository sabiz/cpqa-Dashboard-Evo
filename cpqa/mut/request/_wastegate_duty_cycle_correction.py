from cpqa.mut.request import MutRequest


class WastegateDutyCycleCorrection(MutRequest):
    @property
    def name(self):
        return "WastegateDutyCycleCorrection"

    @property
    def name_short(self):
        return "WGDCCorr"

    @property
    def request_id(self):
        return 0x8B

    @property
    def unit(self):
        return "%"

    @property
    def max(self):
        return 50

    @property
    def min(self):
        return -50

    def convert(self, x):
        return 0.5 * x - 64
