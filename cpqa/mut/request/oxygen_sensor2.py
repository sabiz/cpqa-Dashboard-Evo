from cpqa.mut.request import MutRequest


class OxygenSensor2(MutRequest):
    @property
    def name(self):
        return "OxygenSensor2"

    @property
    def name_short(self):
        return "O2Sensor2"

    @property
    def request_id(self):
        return 0x3C

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
