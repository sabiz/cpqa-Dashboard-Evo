import time
import math
import random
from cpqa.mut import MutResult


class MutMock:
    def __init__(self, vendor_id, product_id):
        self.__count = 0
        pass

    def open(self, index):
        time.sleep(3)
        return MutResult(0, MutResult.STATUS_OK, True)

    def close(self):
        return MutResult(0, MutResult.STATUS_OK, True)

    def request(self, request_id):
        time.sleep(0.05)

        self.__count += 0.0001
        return MutResult(
            (abs(math.sin(self.__count)) + random.random() / 2.0 * 255),
            MutResult.STATUS_OK,
            True,
        )
        # return MutResult(0, MutResult.STATUS_OK, True)

    @property
    def device_count(self):
        time.sleep(0.01)
        return MutResult(1, MutResult.STATUS_OK, True)
