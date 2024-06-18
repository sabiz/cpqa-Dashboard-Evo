from cpqa.mut.request import MutRequest


class IscSteps(MutRequest):
    @property
    def name(self):
        return "IscSteps"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x16

    @property
    def unit(self):
        return "steps"

    @property
    def max(self):
        return 255

    @property
    def min(self):
        return 0

    def convert(self, x):
        return x
