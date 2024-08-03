from cpqa.mut.request import MutRequest


class WastegateDutyCycle(MutRequest):
    @property
    def name(self):
        return "WastegateDutyCycle"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x86

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
        return x / 2
