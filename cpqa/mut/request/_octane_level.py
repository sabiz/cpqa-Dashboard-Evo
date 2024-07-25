from cpqa.mut.request import MutRequest


class OctaneLevel(MutRequest):
    @property
    def name(self):
        return "OctaneLevel"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x27

    @property
    def unit(self):
        return "%"

    @property
    def max(self):
        return 100

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 100 * x / 255
