from .__mut_mock import MutMock
from .__mut_native_proxy import MutNativeProxy as Mut
from cpqa.common.log import log_i
from cpqa.common.log import log_d
from cpqa.common.log import log_e
from cpqa.common.log import log_w
from cpqa.common.settings import Settings
from cpqa.mut.request.multi_mut_request import MultiMutRequest
from cpqa.mut.request.afr_map import AfrMap
from cpqa.mut.request.air_conditioning_relay import AirConditioningRelay
from cpqa.mut.request.air_conditioning_switch import AirConditioningSwitch
from cpqa.mut.request.air_flow_hz import AirFlowHz
from cpqa.mut.request.air_flow_rev import AirFlowRev
from cpqa.mut.request.air_temperature import AirTemperature
from cpqa.mut.request.air_volume import AirVolume
from cpqa.mut.request.barometer import Barometer
from cpqa.mut.request.battery_level import BatteryLevel
from cpqa.mut.request.boost import Boost
from cpqa.mut.request.coolant_temperature import CoolantTemperature
from cpqa.mut.request.crank_signal_switch import CrankSignalSwitch
from cpqa.mut.request.ecu_load import EcuLoad
from cpqa.mut.request.egr_temperature import EgrTemperature
from cpqa.mut.request.engine_rpm import EngineRpm
from cpqa.mut.request.fuel_consumption import FuelConsumption
from cpqa.mut.request.fuel_trim_high import FuelTrimHigh
from cpqa.mut.request.fuel_trim_low import FuelTrimLow
from cpqa.mut.request.fuel_trim_mid import FuelTrimMid
from cpqa.mut.request.gear import Gear
from cpqa.mut.request.idle_position_switch import IdlePositionSwitch
from cpqa.mut.request.inhibitor_switch import InhibitorSwitch
from cpqa.mut.request.injector_duty_cycle import InjectorDutyCycle
from cpqa.mut.request.injector_latency import InjectorLatency
from cpqa.mut.request.injector_pulse_width import InjectorPulseWidth
from cpqa.mut.request.isc_steps import IscSteps
from cpqa.mut.request.knock_sum import KnockSum
from cpqa.mut.request.load_error import LoadError
from cpqa.mut.request.maf_air_temperature import MafAirTemperature
from cpqa.mut.request.octane_level import OctaneLevel
from cpqa.mut.request.oxygen_sensor import OxygenSensor
from cpqa.mut.request.oxygen_sensor2 import OxygenSensor2
from cpqa.mut.request.power_steering_switch import PowerSteeringSwitch
from cpqa.mut.request.speed import Speed
from cpqa.mut.request.target_idle_rpm import TargetIdleRpm
from cpqa.mut.request.throttle_position import ThrottlePosition
from cpqa.mut.request.timing_advance import TimingAdvance
from cpqa.mut.request.wastegate_duty_cycle import WastegateDutyCycle
from cpqa.mut.request.wastegate_duty_cycle_correction import WastegateDutyCycleCorrection


class MutClient:

    __MAX_HISTORY_SIZE = 50
    __MIN_HISTORY_SIZE = 15

    def __init__(self, is_mock):
        vender_id = Settings.get(Settings.Keys.VENDOR_ID)
        product_id = Settings.get(Settings.Keys.PRODUCT_ID)
        log_i("MutClient", f"vendor_id: {vender_id:04x}, product_id: {product_id:04x}")
        if (is_mock):
            self.__mut = MutMock(vender_id, product_id)
        else:
            self.__mut = Mut(vender_id, product_id)
        self.request_history = []

    def open(self, index):
        result = self.__mut.open(index)
        log_d("MutClient", f"open: {result}")
        return result.is_success

    def close(self):
        self.__mut.close()
        log_d("MutClient", "close")

    def request(self, request):
        """
        :param request: MutRequest
        :return: float or None(when connection is lost)
        """

        result = self.__mut.request(request.request_id)
        if not result.is_success:
            log_i("MutClient", f"request failed: {result}")
            return result.status

        if isinstance(request, MultiMutRequest):
            result_values = []
            for i in range(len(request.sub_requests)):
                log_d("MutClient",
                      f"MultiMutRequest: {request.sub_requests[i]}")
                tmp = self.request(request.sub_requests[i])
                result_values.append(tmp)
            request.sub_values = result_values

        resultValue = request.convert(result.value)
        log_d("MutClient", f"MutRequest {request.name_short}:\t{resultValue}")

        has_connection = self.__check_connection(result.value)
        if not has_connection:
            log_i("MutClient", "Connection lost")
            return None

        return resultValue

    def exist_device(self):
        result = self.__mut.device_count
        return result.value > 0

    def __check_connection(self, value):
        # [Checking connection]
        # If the connection is lost,
        # response will be same regardless of MUT request.
        self.request_history.append(value)

        if len(self.request_history) < MutClient.__MIN_HISTORY_SIZE:
            return True

        if len(self.request_history) > MutClient.__MAX_HISTORY_SIZE:
            self.request_history.pop(0)

        unique_values = list(set(self.request_history))
        return len(unique_values) != 1

    __KEY_TO_REQUEST_MAP = {
        Settings.Keys.REQUEST_AFR_MAP: AfrMap(),
        Settings.Keys.REQUEST_AIR_CONDITIONING_RELAY: AirConditioningRelay(),
        Settings.Keys.REQUEST_AIR_CONDITIONING_SWITCH: AirConditioningSwitch(),
        Settings.Keys.REQUEST_AIR_FLOW_HZ: AirFlowHz(),
        Settings.Keys.REQUEST_AIR_FLOW_REV: AirFlowRev(),
        Settings.Keys.REQUEST_AIR_TEMPERATURE: AirTemperature(),
        Settings.Keys.REQUEST_AIR_VOLUME: AirVolume(),
        Settings.Keys.REQUEST_BAROMETER: Barometer(),
        Settings.Keys.REQUEST_BATTERY_LEVEL: BatteryLevel(),
        Settings.Keys.REQUEST_BOOST: Boost(),
        Settings.Keys.REQUEST_COOLANT_TEMPERATURE: CoolantTemperature(),
        Settings.Keys.REQUEST_CRANK_SIGNAL_SWITCH: CrankSignalSwitch(),
        Settings.Keys.REQUEST_ECU_LOAD: EcuLoad(),
        Settings.Keys.REQUEST_EGR_TEMPERATURE: EgrTemperature(),
        Settings.Keys.REQUEST_ENGINE_RPM: EngineRpm(),
        Settings.Keys.REQUEST_FUEL_CONSUMPTION: FuelConsumption(),
        Settings.Keys.REQUEST_FUEL_TRIM_HIGH: FuelTrimHigh(),
        Settings.Keys.REQUEST_FUEL_TRIM_LOW: FuelTrimLow(),
        Settings.Keys.REQUEST_FUEL_TRIM_MID: FuelTrimMid(),
        Settings.Keys.REQUEST_GEAR: Gear(),
        Settings.Keys.REQUEST_IDLE_POSITION_SWITCH: IdlePositionSwitch(),
        Settings.Keys.REQUEST_INHIBITOR_SWITCH: InhibitorSwitch(),
        Settings.Keys.REQUEST_INJECTOR_DUTY_CYCLE: InjectorDutyCycle(),
        Settings.Keys.REQUEST_INJECTOR_LATENCY: InjectorLatency(),
        Settings.Keys.REQUEST_INJECTOR_PULSE_WIDTH: InjectorPulseWidth(),
        Settings.Keys.REQUEST_ISC_STEPS: IscSteps(),
        Settings.Keys.REQUEST_KNOCK_SUM: KnockSum(),
        Settings.Keys.REQUEST_LOAD_ERROR: LoadError(),
        Settings.Keys.REQUEST_MAF_AIR_TEMPERATURE: MafAirTemperature(),
        Settings.Keys.REQUEST_OCTANE_LEVEL: OctaneLevel(),
        Settings.Keys.REQUEST_OXYGEN_SENSOR: OxygenSensor(),
        Settings.Keys.REQUEST_OXYGEN_SENSOR2: OxygenSensor2(),
        Settings.Keys.REQUEST_POWER_STEERING_SWITCH: PowerSteeringSwitch(),
        Settings.Keys.REQUEST_SPEED: Speed(),
        Settings.Keys.REQUEST_TARGET_IDLE_RPM: TargetIdleRpm(),
        Settings.Keys.REQUEST_THROTTLE_POSITION: ThrottlePosition(),
        Settings.Keys.REQUEST_TIMING_ADVANCE: TimingAdvance(),
        Settings.Keys.REQUEST_WASTEGATE_DUTY_CYCLE: WastegateDutyCycle(),
        Settings.Keys.REQUEST_WASTEGATE_DUTY_CYCLE_CORRECTION:
            WastegateDutyCycleCorrection()
    }

    @staticmethod
    def settings_key_to_request_instance(key):
        return MutClient.__KEY_TO_REQUEST_MAP[key]
