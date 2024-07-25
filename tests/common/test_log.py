import logging
import cpqa
from cpqa.common import log_init
from cpqa.common import log_d
from cpqa.common import Keys


def test_log_init(mocker):
    def settings_get(level):
        def settings_get_impl(x):
            if x == Keys.LOG_LEVEL_STREAM:
                return level
            elif x == Keys.LOG_LEVEL_FILE:
                return logging.CRITICAL + 10
            elif x == Keys.LOG_FILE_NAME:
                return "test.log"
            elif x == Keys.LOG_FILE_SIZE:
                return 100000
            elif x == Keys.LOG_FILE_HISTORY_COUNT:
                return 5

        return settings_get_impl

    log_d("test", "msg")

    mocker.patch(
        "cpqa.common._settings.Settings.get", side_effect=settings_get(logging.ERROR)
    )
    log_init()
    assert cpqa.common._log.log_file_history_count == 5
    assert cpqa.common._log.log_file_size == 100000
    assert cpqa.common._log.log_file_name == "test.log"
    assert cpqa.common._log.file_log_level == logging.CRITICAL + 10
    assert cpqa.common._log.stream_log_level == logging.ERROR

    mocker.patch("cpqa.common._log.initialized", False)
    mocker.patch(
        "cpqa.common._settings.Settings.get", side_effect=settings_get(logging.WARNING)
    )
    log_init()
    assert cpqa.common._log.stream_log_level == logging.WARNING

    mocker.patch("cpqa.common._log.initialized", False)
    mocker.patch(
        "cpqa.common._settings.Settings.get", side_effect=settings_get(logging.INFO)
    )
    log_init()
    assert cpqa.common._log.stream_log_level == logging.INFO

    mocker.patch("cpqa.common._log.initialized", False)
    mocker.patch(
        "cpqa.common._settings.Settings.get", side_effect=settings_get(logging.DEBUG)
    )
    log_init()
    assert cpqa.common._log.stream_log_level == logging.DEBUG

    mocker.patch(
        "cpqa.common._settings.Settings.get", side_effect=settings_get(logging.ERROR)
    )
    log_init()
    assert cpqa.common._log.stream_log_level == logging.DEBUG
