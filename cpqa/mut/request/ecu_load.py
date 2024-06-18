from cpqa.mut.request import MutRequest


class EcuLoad(MutRequest):
    @property
    def name(self):
        return "EcuLoad"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x1C

    @property
    def unit(self):
        return "/160"

    @property
    def max(self):
        return 160

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 5 * x / 8
