from cpqa.mut.request import MutRequest


class EngineRpm(MutRequest):
    @property
    def name(self):
        return "EngineRPM"

    @property
    def name_short(self):
        return "RPM"

    @property
    def request_id(self):
        return 0x21

    @property
    def unit(self):
        return "rpm"

    @property
    def max(self):
        return 80

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 31.25 * x
