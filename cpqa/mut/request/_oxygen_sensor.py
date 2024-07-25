from cpqa.mut.request import MutRequest


class OxygenSensor(MutRequest):
    @property
    def name(self):
        return "OxygenSensor"

    @property
    def name_short(self):
        return "O2Sensor"

    @property
    def request_id(self):
        return 0x13

    @property
    def unit(self):
        return "V"

    @property
    def max(self):
        return 5

    @property
    def min(self):
        return 0

    def convert(self, x):
        return 0.01952 * x
