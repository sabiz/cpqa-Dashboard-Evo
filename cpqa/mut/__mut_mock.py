import time
import random
from cpqa.mut.mut_result import MutResult


class MutMock:

    def __init__(self, vendor_id, product_id):
        self.device_count = MutResult(1, MutResult.STATUS_OK, True)

    def open(self, index):
        time.sleep(3)
        return MutResult(0, MutResult.STATUS_OK, True)

    def close(self):
        return MutResult(0, MutResult.STATUS_OK, True)

    def request(self, request_id):
        time.sleep(0.05)
        return MutResult(random.randint(0, 255), MutResult.STATUS_OK, True)
