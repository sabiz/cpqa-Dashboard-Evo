from cpqa.mut.request import MutRequest
from cpqa.mut.request import MultiMutRequest
from cpqa.mut.request import Speed


class Gear(MutRequest, MultiMutRequest):

    def __init__(self):
        MutRequest.__init__(self)
        MultiMutRequest.__init__(self)
        self.__sub_requests = [Speed()]

    @property
    def name(self):
        return "Gear"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x21

    @property
    def unit(self):
        return " "

    @property
    def max(self):
        return 255

    @property
    def min(self):
        return 0

    @property
    def sub_requests(self):
        return self.__sub_requests

    def convert(self, x):
        if self._sub_values[0] == 0:
            return 0
        return x / self._sub_values[0]
