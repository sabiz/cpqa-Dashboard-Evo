from datetime import datetime
from kivy.logger import Logger


def log_d(tag, msg):
    Logger.debug(f'{tag}: [{__time()}] {msg}')


def log_i(tag, msg):
    Logger.info(f'{tag}: [{__time()}] {msg}')


def log_w(tag, msg):
    Logger.warning(f'{tag}: [{__time()}] {msg}')


def log_e(tag, msg):
    Logger.error(f'{tag}: [{__time()}] {msg}')


def __time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
