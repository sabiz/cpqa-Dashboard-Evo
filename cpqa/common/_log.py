import logging
from concurrent_log_handler import ConcurrentRotatingFileHandler
from pathlib import Path

logger_map = {}

initialized = False
stream_log_level = logging.DEBUG
file_log_level = logging.DEBUG
log_file_name = None
log_file_size = None
log_file_history_count = None


def __create_handlers(need_stream_handler, need_file_handler):
    format_str = "%(asctime)s %(levelname)s [%(name)s]: %(message)s"
    if need_stream_handler:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(stream_log_level)
        stream_handler.setFormatter(logging.Formatter(format_str))
    else:
        stream_handler = None

    if need_file_handler:
        if (
            log_file_name is None
            or log_file_size is None
            or log_file_history_count is None
        ):
            raise ValueError("log file name, size, and history count must be set")

        log_file_name_path = Path(log_file_name)
        log_file_name_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = ConcurrentRotatingFileHandler(
            log_file_name, maxBytes=log_file_size, backupCount=log_file_history_count
        )
        file_handler.setFormatter(logging.Formatter(format_str))
        file_handler.setLevel(file_log_level)
    else:
        file_handler = None

    return (stream_handler, file_handler)


def log_init():
    from cpqa.common import Settings
    from cpqa.common import Keys

    global initialized
    if initialized:
        return
    settings = Settings()
    global stream_log_level
    global file_log_level
    global log_file_name
    global log_file_size
    global log_file_history_count
    stream_level = settings.get(Keys.LOG_LEVEL_STREAM)
    file_level = settings.get(Keys.LOG_LEVEL_FILE)
    stream_log_level = stream_level if stream_level is not None else logging.DEBUG
    file_log_level = file_level if file_level is not None else logging.DEBUG
    log_file_name = settings.get(Keys.LOG_FILE_NAME)
    log_file_size = settings.get(Keys.LOG_FILE_SIZE)
    log_file_history_count = settings.get(Keys.LOG_FILE_HISTORY_COUNT)
    for logger in logger_map.values():
        logger.setLevel(stream_log_level)
        for h in logger.handlers:
            if h.__class__ == logging.StreamHandler:
                h.setLevel(stream_log_level)
            else:
                logger.removeHandler(h)
        _, file_handler = __create_handlers(False, True)
        logger.addHandler(file_handler)

    initialized = True


def log_d(tag, msg):
    logger = __get_logger(tag)
    logger.debug(msg)


def log_i(tag, msg):
    logger = __get_logger(tag)
    logger.info(msg)


def log_w(tag, msg):
    logger = __get_logger(tag)
    logger.warning(msg)


def log_e(tag, msg):
    logger = __get_logger(tag)
    logger.error(msg)


def __get_logger(tag):
    if tag in logger_map:
        return logger_map[tag]

    logger = logging.getLogger(tag)
    logger.propagate = False
    logger.setLevel(stream_log_level)
    stream_handler = None
    file_handler = None
    if not initialized:
        stream_handler, file_handler = __create_handlers(True, False)
    else:
        stream_handler, file_handler = __create_handlers(True, True)
    if stream_handler is not None:
        logger.addHandler(stream_handler)
    if file_handler is not None:
        logger.addHandler(file_handler)
    logger_map[tag] = logger
    return logger
