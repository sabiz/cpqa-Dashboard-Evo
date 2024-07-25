from cpqa.mut.request import MutRequest


class TargetIdleRpm(MutRequest):
    @property
    def name(self):
        return "TargetIdleRpm"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x24

    @property
    def unit(self):
        return "rpm"

    @property
    def max(self):
        return 8000

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 7.8 * x
