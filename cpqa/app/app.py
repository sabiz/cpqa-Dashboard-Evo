from pathlib import Path
from collections import namedtuple
from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from cpqa.app.ui.auto_fit_label import AutoFitLabel
from cpqa.app.ui.power_button import PowerButton
from cpqa.app.ui.value_name_label import ValueNameLabel
from cpqa.common.log import log_d
from cpqa.common.log import log_i
from cpqa.common.log import log_w
from cpqa.common.settings import Settings
from cpqa.mut.mut_client import MutClient

RequestJob = namedtuple("RequestJob", ("request", "interval"))


class CpqaApp(App):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mut_client = None
        self.screen_manager = None
        self.request_table = []
        self.current_index = 0
        self.request_schedule = None

    def build(self):
        self.icon = 'icon.png'
        'res/icon.png'
        Settings.load()
        main_screen = CpqaApp.MainScreen(name='main')
        main_screen.on_tap_value_name_label_callback = self.change_request
        main_screen.power_button_before_callback = self.on_before_poweroff
        self.screen_manager = ScreenManager(transition=FadeTransition())
        self.screen_manager.add_widget(CpqaApp.InitScreen(name='init'))
        self.screen_manager.add_widget(main_screen)

        mut_mock = Settings.get(Settings.Keys.MUT_MOCK)
        log_i("CpqaApp", f"mut_mock: {mut_mock}")
        self.mut_client = MutClient(mut_mock)

        return self.screen_manager

    def on_start(self):
        self.__load_request_settings()
        Clock.schedule_once(self.find_device, 0.3)

    def find_device(self, dt):
        log_d("CpqaApp", "Find Device")

        # Waiting for device connection
        if not self.mut_client.exist_device():
            log_d("CpqaApp", "Device not found")
            Clock.schedule_once(self.find_device, 0.3)
            return

        Clock.schedule_once(self.open_device, 0.3)

    def open_device(self, dt):
        log_d("CpqaApp", "Open Device")
        device_index = Settings.get(Settings.Keys.DEVICE_INDEX)
        log_d("CpqaApp", f"device_index: {device_index}")
        result = self.mut_client.open(device_index)
        if not result:
            log_w("CpqaApp", "Device open failed")
            self.find_device(0)
            return
        log_i("CpqaApp", "Device open success")
        Clock.schedule_once(self.start_request, 0.3)

    def start_request(self, dt):
        log_d("CpqaApp", "Start Request")
        if self.screen_manager.current_screen.name != "main":
            self.screen_manager.switch_to(
                self.screen_manager.get_screen("main"))

        clock_event = Clock.schedule_interval(
            lambda dt: self.process_mut_request(
                self.request_table[self.current_index].request),
            self.request_table[self.current_index].interval / 1000.0)
        self.request_schedule = clock_event

    def process_mut_request(self, request):
        log_d("CpqaApp", "Process MUT Request")
        val = self.mut_client.request(request)
        self.screen_manager.get_screen("main").on_update_value(
            request, val)

    def change_request(self):
        log_d("CpqaApp", "Change Request")
        self.request_schedule.cancel()
        self.current_index = (self.current_index + 1) % len(self.request_table)
        self.start_request(0)

    def on_before_poweroff(self):
        log_i("CpqaApp", "OnBeforePoweroff")
        self.request_schedule.cancel()
        self.mut_client.close()
        Clock.schedule_once(self.stop, 1)

    def __load_request_settings(self):
        for key in Settings.REQUEST_KEY_LIST:
            request = Settings.get(key)
            if not request.enabled:
                continue
            self.request_table.append(
                RequestJob(
                    MutClient.settings_key_to_request_instance(key),
                    request.interval))

    class InitScreen(Screen):
        pass

    class MainScreen(Screen):
        value_label = ObjectProperty(AutoFitLabel)
        value_unit_label = ObjectProperty(AutoFitLabel)
        value_name_label = ObjectProperty(ValueNameLabel)
        power_button = ObjectProperty(PowerButton)

        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.value_name_label.set_on_tap_func(self.on_tap_value_name_label)
            self.power_button_before_callback = None
            power_button_command = Settings.get(
                Settings.Keys.POWER_BUTTON_COMMAND)
            log_i("Settings", f"power_button_command: {power_button_command}")
            self.power_button.set_command(power_button_command)
            self.power_button.set_before_callback(
                    lambda: self.power_button_before_callback())

            self.on_tap_value_name_label_callback = None

        def on_tap_value_name_label(self, touch):
            log_d('MainScreen', touch)
            if self.on_tap_value_name_label_callback is not None:
                self.on_tap_value_name_label_callback()

        def on_update_value(self, request, value):
            self.value_label.text = str(round(value, 2))
            self.value_unit_label.text = request.unit
            self.value_name_label.text = request.name
