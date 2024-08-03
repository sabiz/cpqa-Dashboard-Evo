from cpqa.mut.request import MutRequest


class LoadError(MutRequest):
    @property
    def name(self):
        return "LoadError"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x8A

    @property
    def unit(self):
        return "load"

    @property
    def max(self):
        return 25

    @property
    def min(self):
        return -25

    def convert(self, x):
        return 0.15625 * x - 20
