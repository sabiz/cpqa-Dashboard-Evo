from cpqa.native.mut import Mut
from cpqa.common.log import log_i
from cpqa.common.log import log_d
from cpqa.common.log import log_e
from cpqa.common.log import log_w
from cpqa.mut.mut_result import MutResult

class MutNativeProxy:

    __NATIVE_LOG_LEVEL_VERBOSE = 0
    __NATIVE_LOG_LEVEL_INFO = 1
    __NATIVE_LOG_LEVEL_WARNING = 2
    __NATIVE_LOG_LEVEL_ERROR = 3

    def __init__(self, vendor_id, product_id):
        self.__mut = Mut(vendor_id, product_id, self.__native_log)

    def open(self, index):
        result = self.__mut.open(index)
        return MutNativeProxy.__toMutResult(result)

    def close(self):
        result = self.__mut.close()
        return MutNativeProxy.__toMutResult(result)

    def request(self, request_id):
        result = self.__mut.request(request_id)
        return MutNativeProxy.__toMutResult(result)

    @property
    def device_count(self):
        result = self.__mut.device_count()
        return MutNativeProxy.__toMutResult(result)

    @staticmethod
    def __toMutResult(result):
        return MutResult(result.get('value'), result['status'], result['status'] == MutResult.STATUS_OK)

    @staticmethod
    def __native_log(level, msg):
        if level == MutNativeProxy.__NATIVE_LOG_LEVEL_VERBOSE:
            log_d("MutNativeProxy", msg)
        elif level == MutNativeProxy.__NATIVE_LOG_LEVEL_INFO:
            log_i("MutNativeProxy", msg)
        elif level == MutNativeProxy.__NATIVE_LOG_LEVEL_WARNING:
            log_w("MutNativeProxy", msg)
        elif level == MutNativeProxy.__NATIVE_LOG_LEVEL_ERROR:
            log_e("MutNativeProxy", msg)