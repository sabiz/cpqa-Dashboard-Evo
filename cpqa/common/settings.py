from collections import namedtuple
from pathlib import Path
from enum import Enum
from kivy.config import Config

KeyConf = namedtuple("KeyConf", ("key", "value_type"))
RequestSetting = namedtuple("RequestSetting", ("enabled", "interval"))


class Settings:

    CONFIG_SECTION = "cpqa"

    @staticmethod
    def load():
        config_path = (Path(__file__).parent
                       .parent.parent.absolute() / 'config.ini')
        Config.read(str(config_path))

    @staticmethod
    def get(key):
        key_conf = key.value
        if key_conf.value_type == "str":
            return Config.get(Settings.CONFIG_SECTION, key_conf.key)
        elif key_conf.value_type == "bool":
            value = Config.get(Settings.CONFIG_SECTION, key_conf.key)
            return value.lower() == "true" or value == "1"
        elif key_conf.value_type == "hex":
            return int(Config.get(Settings.CONFIG_SECTION, key_conf.key), 16)
        elif key_conf.value_type == "int":
            return int(Config.get(Settings.CONFIG_SECTION, key_conf.key))
        elif key_conf.value_type == "request":
            value = Config.get(
                Settings.CONFIG_SECTION, key_conf.key).split(",")
            return RequestSetting(int(value[0]) > 0, int(value[1]))

    class Keys(Enum):
        POWER_BUTTON_COMMAND = KeyConf("power_button_command", "str")
        MUT_MOCK = KeyConf("mut_mock", "bool")
        DEVICE_INDEX = KeyConf("device_index", "int")
        VENDOR_ID = KeyConf("vendor_id", "hex")
        PRODUCT_ID = KeyConf("product_id", "hex")
        BAUD_RATE = KeyConf("baud_rate", "int")

        REQUEST_AFR_MAP = KeyConf("request_afr_map", "request")
        REQUEST_AIR_CONDITIONING_RELAY = KeyConf(
            "request_air_conditioning_relay", "request")
        REQUEST_AIR_CONDITIONING_SWITCH = KeyConf(
            "request_air_conditioning_switch", "request")
        REQUEST_AIR_FLOW_HZ = KeyConf("request_air_flow_hz", "request")
        REQUEST_AIR_FLOW_REV = KeyConf("request_air_flow_rev", "request")
        REQUEST_AIR_TEMPERATURE = KeyConf("request_air_temperature", "request")
        REQUEST_AIR_VOLUME = KeyConf("request_air_volume", "request")
        REQUEST_BAROMETER = KeyConf("request_barometer", "request")
        REQUEST_BATTERY_LEVEL = KeyConf("request_battery_level", "request")
        REQUEST_BOOST = KeyConf("request_boost", "request")
        REQUEST_COOLANT_TEMPERATURE = KeyConf(
            "request_coolant_temperature", "request")
        REQUEST_CRANK_SIGNAL_SWITCH = KeyConf(
            "request_crank_signal_switch", "request")
        REQUEST_ECU_LOAD = KeyConf("request_ecu_load", "request")
        REQUEST_EGR_TEMPERATURE = KeyConf("request_egr_temperature", "request")
        REQUEST_ENGINE_RPM = KeyConf("request_engine_rpm", "request")
        REQUEST_FUEL_CONSUMPTION = KeyConf(
            "request_fuel_consumption", "request")
        REQUEST_FUEL_TRIM_HIGH = KeyConf("request_fuel_trim_high", "request")
        REQUEST_FUEL_TRIM_LOW = KeyConf("request_fuel_trim_low", "request")
        REQUEST_FUEL_TRIM_MID = KeyConf("request_fuel_trim_mid", "request")
        REQUEST_GEAR = KeyConf("request_gear", "request")
        REQUEST_IDLE_POSITION_SWITCH = KeyConf(
            "request_idle_position_switch", "request")
        REQUEST_INHIBITOR_SWITCH = KeyConf(
            "request_inhibitor_switch", "request")
        REQUEST_INJECTOR_DUTY_CYCLE = KeyConf(
            "request_injector_duty_cycle", "request")
        REQUEST_INJECTOR_LATENCY = KeyConf(
            "request_injector_latency", "request")
        REQUEST_INJECTOR_PULSE_WIDTH = KeyConf(
            "request_injector_pulse_width", "request")
        REQUEST_ISC_STEPS = KeyConf("request_isc_steps", "request")
        REQUEST_KNOCK_SUM = KeyConf("request_knock_sum", "request")
        REQUEST_LOAD_ERROR = KeyConf("request_load_error", "request")
        REQUEST_MAF_AIR_TEMPERATURE = KeyConf(
            "request_maf_air_temperature", "request")
        REQUEST_OCTANE_LEVEL = KeyConf("request_octane_level", "request")
        REQUEST_OXYGEN_SENSOR = KeyConf("request_oxygen_sensor", "request")
        REQUEST_OXYGEN_SENSOR2 = KeyConf("request_oxygen_sensor2", "request")
        REQUEST_POWER_STEERING_SWITCH = KeyConf(
            "request_power_steering_switch", "request")
        REQUEST_SPEED = KeyConf("request_speed", "request")
        REQUEST_TARGET_IDLE_RPM = KeyConf("request_target_idle_rpm", "request")
        REQUEST_THROTTLE_POSITION = KeyConf(
            "request_throttle_position", "request")
        REQUEST_TIMING_ADVANCE = KeyConf("request_timing_advance", "request")
        REQUEST_WASTEGATE_DUTY_CYCLE = KeyConf(
            "request_wastegate_duty_cycle", "request")
        REQUEST_WASTEGATE_DUTY_CYCLE_CORRECTION = KeyConf(
            "request_wastegate_duty_cycle_correction", "request")

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
        Keys.REQUEST_WASTEGATE_DUTY_CYCLE_CORRECTION
    ]
