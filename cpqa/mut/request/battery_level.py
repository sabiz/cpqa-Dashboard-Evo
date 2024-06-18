from cpqa.mut.request import MutRequest


class BatteryLevel(MutRequest):
    @property
    def name(self):
        return "BatteryLevel"

    @property
    def name_short(self):
        return "Battery"

    @property
    def request_id(self):
        return 0x14

    @property
    def unit(self):
        return "V"

    @property
    def max(self):
        return 16

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 0.07333 * x
