from cpqa.mut.request import MutRequest
from cpqa.mut.request import MultiMutRequest
from cpqa.mut.request import InjectorPulseWidth
from cpqa.mut.request import Speed


class FuelConsumption(MutRequest, MultiMutRequest):

    __HISTORY_SIZE = 100

    def __init__(self):
        MutRequest.__init__(self)
        MultiMutRequest.__init__(self)
        self.__sub_requests = [InjectorPulseWidth(), Speed()]
        self.__history = []
        self.__last_value = 0

    @property
    def name(self):
        return "FuelConsumption"

    @property
    def name_short(self):
        return self.name

    @property
    def request_id(self):
        return 0x21

    @property
    def unit(self):
        return "km/L"

    @property
    def max(self):
        return 50

    @property
    def min(self):
        return 0

    @property
    def sub_requests(self):
        return self.__sub_requests

    def convert(self, x):
        if len(self._sub_values) < 2 or self._sub_values[1] == 0:
            return self.__last_value

        tmp = (31.25 * x * self._sub_values[0] * 20 * 6
               / self._sub_values[1] / 1200)

        if tmp <= 0:
            return self.__last_value

        self.__last_value = self.__moving_average(100 / tmp)
        return self.__last_value

    def __moving_average(self, value):
        self.__history.append(value)
        if len(self.__history) > FuelConsumption.__HISTORY_SIZE:
            self.__history.pop(0)
        return sum(self.__history) / len(self.__history)
