from abc import ABCMeta, abstractmethod


class MutRequest(metaclass=ABCMeta):

    @property
    @abstractmethod
    def name(self):
        pass

    @property
    @abstractmethod
    def name_short(self):
        pass

    @property
    @abstractmethod
    def request_id(self):
        pass

    @property
    @abstractmethod
    def unit(self):
        pass

    @property
    @abstractmethod
    def max(self):
        pass

    @property
    @abstractmethod
    def min(self):
        pass

    @abstractmethod
    def convert(self, x):
        pass
