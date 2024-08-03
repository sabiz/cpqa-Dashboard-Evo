from cpqa.mut.request import InjectorPulseWidth
from cpqa.mut.request import MutRequest
from cpqa.mut.request import MultiMutRequest


class InjectorDutyCycle(MutRequest, MultiMutRequest):

    def __init__(self):
        MutRequest.__init__(self)
        MultiMutRequest.__init__(self)
        self.__sub_requests = [InjectorPulseWidth()]

    @property
    def name(self):
        return "InjectorDutyCycle"

    @property
    def name_short(self):
        return "InjDutyCycle"

    @property
    def request_id(self):
        return 0x21

    @property
    def unit(self):
        return "%"

    @property
    def max(self):
        return 160

    @property
    def min(self):
        return 0

    @property
    def sub_requests(self):
        return self.__sub_requests

    def convert(self, x):
        return self.sub_values[0] * 31.25 * x / 1200
