from abc import ABCMeta, abstractmethod


class MultiMutRequest(metaclass=ABCMeta):

    def __init__(self):
        self._sub_values = []

    @property
    @abstractmethod
    def sub_requests(self):
        pass

    @property
    def sub_values(self):
        return self._sub_values

    @sub_values.setter
    def sub_values(self, x):
        if len(x) != len(self.sub_requests):
            raise ValueError(
                "Length of sub_values must be equal to length of sub_requests")
        self._sub_values = x
