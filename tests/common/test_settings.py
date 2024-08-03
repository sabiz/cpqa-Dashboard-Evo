from cpqa.common import Settings
from cpqa.common import Keys


def test_settings_load(mocker):
    settings = Settings()
    settings.load()

    assert settings._Settings__settings is not None
