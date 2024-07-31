from pip._vendor import tomli as tomllib
import logging
from collections import namedtuple
from pathlib import Path
from enum import Enum
from cpqa.common import log_d
from cpqa.common import log_w

SettingsKey = namedtuple("SettingsKey", ("section", "key", "value_type"))
RequestSetting = namedtuple("RequestSetting", ("enabled", "interval"))

LOG_TAG = "Settings"


class Keys(Enum):
    LOG_LEVEL_STREAM = SettingsKey("log", "log_level_stream", "loglevel")
    LOG_LEVEL_FILE = SettingsKey("log", "log_level_file", "loglevel")
    LOG_FILE_NAME = SettingsKey("log", "log_file_name", str)
    LOG_FILE_SIZE = SettingsKey("log", "log_file_size", int)
    LOG_FILE_HISTORY_COUNT = SettingsKey("log", "log_file_history_count", int)

    WINDOW_WIDTH = SettingsKey("app", "window_width", int)
    WINDOW_HEIGHT = SettingsKey("app", "window_height", int)
    USE_FRAME_BUFFER = SettingsKey("app", "use_frame_buffer", bool)
    FRAME_BUFFER_PATH = SettingsKey("app", "frame_buffer_path", str)
    POWER_BUTTON_COMMAND = SettingsKey("app", "power_button_command", str)

    USE_MOCK = SettingsKey("mut", "use_mock", bool)
    VENDOR_ID = SettingsKey("mut", "vendor_id", int)
    PRODUCT_ID = SettingsKey("mut", "product_id", int)
    DEVICE_INDEX = SettingsKey("mut", "device_index", int)

    REQUEST_AFR_MAP = SettingsKey("request", "afr_map", "request")
    REQUEST_AIR_CONDITIONING_RELAY = SettingsKey(
        "request", "air_conditioning_relay", "request"
    )
    REQUEST_AIR_CONDITIONING_SWITCH = SettingsKey(
        "request", "air_conditioning_switch", "request"
    )
    REQUEST_AIR_FLOW_HZ = SettingsKey("request", "air_flow_hz", "request")
    REQUEST_AIR_FLOW_REV = SettingsKey("request", "air_flow_rev", "request")
    REQUEST_AIR_TEMPERATURE = SettingsKey("request", "air_temperature", "request")
    REQUEST_AIR_VOLUME = SettingsKey("request", "air_volume", "request")
    REQUEST_BAROMETER = SettingsKey("request", "barometer", "request")
    REQUEST_BATTERY_LEVEL = SettingsKey("request", "battery_level", "request")
    REQUEST_BOOST = SettingsKey("request", "boost", "request")
    REQUEST_COOLANT_TEMPERATURE = SettingsKey(
        "request", "coolant_temperature", "request"
    )
    REQUEST_CRANK_SIGNAL_SWITCH = SettingsKey(
        "request", "crank_signal_switch", "request"
    )
    REQUEST_ECU_LOAD = SettingsKey("request", "ecu_load", "request")
    REQUEST_EGR_TEMPERATURE = SettingsKey("request", "egr_temperature", "request")
    REQUEST_ENGINE_RPM = SettingsKey("request", "engine_rpm", "request")
    REQUEST_FUEL_CONSUMPTION = SettingsKey("request", "fuel_consumption", "request")
    REQUEST_FUEL_TRIM_HIGH = SettingsKey("request", "fuel_trim_high", "request")
    REQUEST_FUEL_TRIM_LOW = SettingsKey("request", "fuel_trim_low", "request")
    REQUEST_FUEL_TRIM_MID = SettingsKey("request", "fuel_trim_mid", "request")
    REQUEST_GEAR = SettingsKey("request", "gear", "request")
    REQUEST_IDLE_POSITION_SWITCH = SettingsKey(
        "request", "idle_position_switch", "request"
    )
    REQUEST_INHIBITOR_SWITCH = SettingsKey("request", "inhibitor_switch", "request")
    REQUEST_INJECTOR_DUTY_CYCLE = SettingsKey(
        "request", "injector_duty_cycle", "request"
    )
    REQUEST_INJECTOR_LATENCY = SettingsKey("request", "injector_latency", "request")
    REQUEST_INJECTOR_PULSE_WIDTH = SettingsKey(
        "request", "injector_pulse_width", "request"
    )
    REQUEST_ISC_STEPS = SettingsKey("request", "isc_steps", "request")
    REQUEST_KNOCK_SUM = SettingsKey("request", "knock_sum", "request")
    REQUEST_LOAD_ERROR = SettingsKey("request", "load_error", "request")
    REQUEST_MAF_AIR_TEMPERATURE = SettingsKey(
        "request", "maf_air_temperature", "request"
    )
    REQUEST_OCTANE_LEVEL = SettingsKey("request", "octane_level", "request")
    REQUEST_OXYGEN_SENSOR = SettingsKey("request", "oxygen_sensor", "request")
    REQUEST_OXYGEN_SENSOR2 = SettingsKey("request", "oxygen_sensor2", "request")
    REQUEST_POWER_STEERING_SWITCH = SettingsKey(
        "request", "power_steering_switch", "request"
    )
    REQUEST_SPEED = SettingsKey("request", "speed", "request")
    REQUEST_TARGET_IDLE_RPM = SettingsKey("request", "target_idle_rpm", "request")
    REQUEST_THROTTLE_POSITION = SettingsKey("request", "throttle_position", "request")
    REQUEST_TIMING_ADVANCE = SettingsKey("request", "timing_advance", "request")
    REQUEST_WASTEGATE_DUTY_CYCLE = SettingsKey(
        "request", "wastegate_duty_cycle", "request"
    )
    REQUEST_WASTEGATE_DUTY_CYCLE_CORRECTION = SettingsKey(
        "request", "wastegate_duty_cycle_correction", "request"
    )


class Settings:
    __instance = None
    __settings = None

    SECTIONS = []
    __KEYS = {}
    __log_level_dict = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARNING,
        "error": logging.ERROR,
    }

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Settings, cls).__new__(cls)

            # Initialize sections and keys
            for k in Keys:
                if k.value.section not in cls.SECTIONS:
                    cls.SECTIONS.append(k.value.section)
                    cls.__KEYS[k.value.section] = []

                cls.__KEYS[k.value.section].append(k.value.key)
        return cls.__instance

    def load(self):
        if self.__settings is not None:
            log_w(LOG_TAG, "Settings already loaded")
            return
        settings_file_path = (
            Path(__file__).parent.parent.parent.absolute() / "settings.toml"
        )
        log_d(LOG_TAG, f"settings file path: {settings_file_path}")
        with open(settings_file_path, "rb") as f:
            self.__settings = tomllib.load(f)
        self.__validate_settings()

    def get(self, key):
        key_conf = key.value
        if key_conf.value_type == "loglevel":
            value = self.__settings[key_conf.section][key_conf.key]
            return Settings.__log_level_dict[value]
        elif (
            key_conf.value_type is str
            or key_conf.value_type is int
            or key_conf.value_type is bool
        ):
            value = self.__settings[key_conf.section][key_conf.key]
            if type(value) is not key_conf.value_type:
                raise ValueError(
                    f"Invalid value type: {key_conf.key} = {value}"
                    f", must be {key_conf.value_type}"
                )
            return value
        elif key_conf.value_type == "request":
            value = self.__settings[key_conf.section][key_conf.key]
            return RequestSetting(value["enabled"], value["interval"])

    def __validate_settings(self):
        for section in self.SECTIONS:
            if section not in self.__settings:
                raise ValueError(f"Missing section: {section}")
            for key in self.__KEYS[section]:
                if key not in self.__settings[section]:
                    raise ValueError(f"Missing key: {key} @ [{section}]")

    # Settings property
    REQUEST_KEY_LIST = [
        Keys.REQUEST_AFR_MAP,
        Keys.REQUEST_AIR_CONDITIONING_RELAY,
        Keys.REQUEST_AIR_CONDITIONING_SWITCH,
        Keys.REQUEST_AIR_FLOW_HZ,
        Keys.REQUEST_AIR_FLOW_REV,
        Keys.REQUEST_AIR_TEMPERATURE,
        Keys.REQUEST_AIR_VOLUME,
        Keys.REQUEST_BAROMETER,
        Keys.REQUEST_BATTERY_LEVEL,
        Keys.REQUEST_BOOST,
        Keys.REQUEST_COOLANT_TEMPERATURE,
        Keys.REQUEST_CRANK_SIGNAL_SWITCH,
        Keys.REQUEST_ECU_LOAD,
        Keys.REQUEST_EGR_TEMPERATURE,
        Keys.REQUEST_ENGINE_RPM,
        Keys.REQUEST_FUEL_CONSUMPTION,
        Keys.REQUEST_FUEL_TRIM_HIGH,
        Keys.REQUEST_FUEL_TRIM_LOW,
        Keys.REQUEST_FUEL_TRIM_MID,
        Keys.REQUEST_GEAR,
        Keys.REQUEST_IDLE_POSITION_SWITCH,
        Keys.REQUEST_INHIBITOR_SWITCH,
        Keys.REQUEST_INJECTOR_DUTY_CYCLE,
        Keys.REQUEST_INJECTOR_LATENCY,
        Keys.REQUEST_INJECTOR_PULSE_WIDTH,
        Keys.REQUEST_ISC_STEPS,
        Keys.REQUEST_KNOCK_SUM,
        Keys.REQUEST_LOAD_ERROR,
        Keys.REQUEST_MAF_AIR_TEMPERATURE,
        Keys.REQUEST_OCTANE_LEVEL,
        Keys.REQUEST_OXYGEN_SENSOR,
        Keys.REQUEST_OXYGEN_SENSOR2,
        Keys.REQUEST_POWER_STEERING_SWITCH,
        Keys.REQUEST_SPEED,
        Keys.REQUEST_TARGET_IDLE_RPM,
        Keys.REQUEST_THROTTLE_POSITION,
        Keys.REQUEST_TIMING_ADVANCE,
        Keys.REQUEST_WASTEGATE_DUTY_CYCLE,
        Keys.REQUEST_WASTEGATE_DUTY_CYCLE_CORRECTION,
    ]
