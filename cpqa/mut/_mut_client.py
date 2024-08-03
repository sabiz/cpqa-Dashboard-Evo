from cpqa.common import log_i
from cpqa.common import log_d
from cpqa.common import log_e
from cpqa.common import log_w
from cpqa.common import Settings
from cpqa.common import Keys
from cpqa.mut.request import MultiMutRequest
from cpqa.mut.request import AfrMap
from cpqa.mut.request import AirConditioningRelay
from cpqa.mut.request import AirConditioningSwitch
from cpqa.mut.request import AirFlowHz
from cpqa.mut.request import AirFlowRev
from cpqa.mut.request import AirTemperature
from cpqa.mut.request import AirVolume
from cpqa.mut.request import Barometer
from cpqa.mut.request import BatteryLevel
from cpqa.mut.request import Boost
from cpqa.mut.request import CoolantTemperature
from cpqa.mut.request import CrankSignalSwitch
from cpqa.mut.request import EcuLoad
from cpqa.mut.request import EgrTemperature
from cpqa.mut.request import EngineRpm
from cpqa.mut.request import FuelConsumption
from cpqa.mut.request import FuelTrimHigh
from cpqa.mut.request import FuelTrimLow
from cpqa.mut.request import FuelTrimMid
from cpqa.mut.request import Gear
from cpqa.mut.request import IdlePositionSwitch
from cpqa.mut.request import InhibitorSwitch
from cpqa.mut.request import InjectorDutyCycle
from cpqa.mut.request import InjectorLatency
from cpqa.mut.request import InjectorPulseWidth
from cpqa.mut.request import IscSteps
from cpqa.mut.request import KnockSum
from cpqa.mut.request import LoadError
from cpqa.mut.request import MafAirTemperature
from cpqa.mut.request import OctaneLevel
from cpqa.mut.request import OxygenSensor
from cpqa.mut.request import OxygenSensor2
from cpqa.mut.request import PowerSteeringSwitch
from cpqa.mut.request import Speed
from cpqa.mut.request import TargetIdleRpm
from cpqa.mut.request import ThrottlePosition
from cpqa.mut.request import TimingAdvance
from cpqa.mut.request import WastegateDutyCycle
from cpqa.mut.request import WastegateDutyCycleCorrection


LOG_TAG = "MutClient"


class MutClient:
    __MAX_HISTORY_SIZE = 50
    __MIN_HISTORY_SIZE = 15

    def __init__(self, use_mock):
        settings = Settings()
        vender_id = settings.get(Keys.VENDOR_ID)
        product_id = settings.get(Keys.PRODUCT_ID)
        log_i(LOG_TAG, f"vendor_id: 0x{vender_id:04x}, product_id: 0x{product_id:04x}")
        if use_mock:
            from cpqa.mut.__mut_mock import MutMock

            self.__mut = MutMock(vender_id, product_id)
        else:  # pragma: no cover
            from cpqa.mut.__mut_native_proxy import MutNativeProxy as Mut

            self.__mut = Mut(vender_id, product_id)
        self.__request_history = []

    def open(self, index):
        if index < 0:
            log_e(LOG_TAG, f"open: index is negative: {index}")
            raise ValueError("index is negative")

        result = self.__mut.open(index)
        if not result.is_success:
            log_w(LOG_TAG, f"open: {result}")
        else:
            log_d(LOG_TAG, f"open: {result}")
        return result

    def close(self):
        result = self.__mut.close()
        if not result.is_success:
            log_w(LOG_TAG, f"close: {result}")
        else:
            log_d(LOG_TAG, "close")

    def request(self, request):
        """
        :param request: MutRequest
        :return: float or None(when connection is lost)
        """

        result = self.__mut.request(request.request_id)
        if not result.is_success:
            log_i(LOG_TAG, f"request failed: {result}")
            return result.status

        if isinstance(request, MultiMutRequest):
            result_values = []
            for i in range(len(request.sub_requests)):
                log_d(LOG_TAG, f"MultiMutRequest: {request.sub_requests[i]}")
                tmp = self.request(request.sub_requests[i])
                result_values.append(tmp)
            request.sub_values = result_values

        resultValue = request.convert(result.value)
        log_d(LOG_TAG, f"MutRequest {request.name_short}:\t{resultValue}")

        has_connection = self.__check_connection(result.value)
        if not has_connection:
            log_i(LOG_TAG, "Connection lost")
            return None

        return resultValue

    def exist_device(self):
        result = self.__mut.device_count
        return result.value > 0

    def __check_connection(self, value):
        # [Checking connection]
        # If the connection is lost,
        # response will be same regardless of MUT request.
        self.__request_history.append(value)

        if len(self.__request_history) < MutClient.__MIN_HISTORY_SIZE:
            return True

        if len(self.__request_history) > MutClient.__MAX_HISTORY_SIZE:
            self.__request_history.pop(0)

        unique_values = list(set(self.__request_history))
        return len(unique_values) != 1

    __KEY_TO_REQUEST_MAP = {
        Keys.REQUEST_AFR_MAP: AfrMap(),
        Keys.REQUEST_AIR_CONDITIONING_RELAY: AirConditioningRelay(),
        Keys.REQUEST_AIR_CONDITIONING_SWITCH: AirConditioningSwitch(),
        Keys.REQUEST_AIR_FLOW_HZ: AirFlowHz(),
        Keys.REQUEST_AIR_FLOW_REV: AirFlowRev(),
        Keys.REQUEST_AIR_TEMPERATURE: AirTemperature(),
        Keys.REQUEST_AIR_VOLUME: AirVolume(),
        Keys.REQUEST_BAROMETER: Barometer(),
        Keys.REQUEST_BATTERY_LEVEL: BatteryLevel(),
        Keys.REQUEST_BOOST: Boost(),
        Keys.REQUEST_COOLANT_TEMPERATURE: CoolantTemperature(),
        Keys.REQUEST_CRANK_SIGNAL_SWITCH: CrankSignalSwitch(),
        Keys.REQUEST_ECU_LOAD: EcuLoad(),
        Keys.REQUEST_EGR_TEMPERATURE: EgrTemperature(),
        Keys.REQUEST_ENGINE_RPM: EngineRpm(),
        Keys.REQUEST_FUEL_CONSUMPTION: FuelConsumption(),
        Keys.REQUEST_FUEL_TRIM_HIGH: FuelTrimHigh(),
        Keys.REQUEST_FUEL_TRIM_LOW: FuelTrimLow(),
        Keys.REQUEST_FUEL_TRIM_MID: FuelTrimMid(),
        Keys.REQUEST_GEAR: Gear(),
        Keys.REQUEST_IDLE_POSITION_SWITCH: IdlePositionSwitch(),
        Keys.REQUEST_INHIBITOR_SWITCH: InhibitorSwitch(),
        Keys.REQUEST_INJECTOR_DUTY_CYCLE: InjectorDutyCycle(),
        Keys.REQUEST_INJECTOR_LATENCY: InjectorLatency(),
        Keys.REQUEST_INJECTOR_PULSE_WIDTH: InjectorPulseWidth(),
        Keys.REQUEST_ISC_STEPS: IscSteps(),
        Keys.REQUEST_KNOCK_SUM: KnockSum(),
        Keys.REQUEST_LOAD_ERROR: LoadError(),
        Keys.REQUEST_MAF_AIR_TEMPERATURE: MafAirTemperature(),
        Keys.REQUEST_OCTANE_LEVEL: OctaneLevel(),
        Keys.REQUEST_OXYGEN_SENSOR: OxygenSensor(),
        Keys.REQUEST_OXYGEN_SENSOR2: OxygenSensor2(),
        Keys.REQUEST_POWER_STEERING_SWITCH: PowerSteeringSwitch(),
        Keys.REQUEST_SPEED: Speed(),
        Keys.REQUEST_TARGET_IDLE_RPM: TargetIdleRpm(),
        Keys.REQUEST_THROTTLE_POSITION: ThrottlePosition(),
        Keys.REQUEST_TIMING_ADVANCE: TimingAdvance(),
        Keys.REQUEST_WASTEGATE_DUTY_CYCLE: WastegateDutyCycle(),
        Keys.REQUEST_WASTEGATE_DUTY_CYCLE_CORRECTION: WastegateDutyCycleCorrection(),
    }

    @staticmethod
    def settings_key_to_request_instance(key):
        return MutClient.__KEY_TO_REQUEST_MAP[key]
