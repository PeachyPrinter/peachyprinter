from kivy.uix.screenmanager import Screen
from kivy.logger import Logger
from kivy.lang import Builder
from ui.custom_widgets import I18NButton
from kivy.app import App

from kivy.clock import Clock

from infrastructure.langtools import _


Builder.load_file('ui/firmware_ui.kv')


class FirmwareUI(Screen):

    def __init__(self, api, **kwargs):
        super(FirmwareUI, self).__init__(**kwargs)
        self.api = api

    def on_enter(self):
        self.firmware_api = self.api.get_firmware_api()
        Logger.info("Required Firmware: {}".format(self.firmware_api.required_version))
        self.required_version = self.firmware_api.required_version
        try:
            Logger.info("Get current firmware")
            self.api.load_printer()
            self.actual_version = self.api.get_configuration_api().get_info_firmware_version_number()
        except:
            Logger.info("Could not get printer information for firmware version check")
            self.actual_version = 'Unknown'
        if self.actual_version == '':
            self.actual_version = 'Older'

    def update_now(self):
        if not self.firmware_api.is_ready():
            self.firmware_api.make_ready()
        self.parent.current = 'firmware_update_ui'


class FirmwareUpdateUI(Screen):
    def __init__(self, api, **kwargs):
        super(FirmwareUpdateUI, self).__init__(**kwargs)
        self.api = api
        self.check_rate = 1.0 / 4.0
        app = App.get_running_app()
        self._complete_button = I18NButton(text_source=_("Close"), on_release=self.close, size_hint_y=None, height=app.button_height)

    def on_enter(self):
        self.image.anim_delay = 1.0 / 30.0
        self.firmware_api = self.api.get_firmware_api()
        Clock.schedule_once(self.ready_check, self.check_rate)

    def close(self, *args):
        self.window.remove_widget(self._complete_button)
        self.parent.current = 'loadingui'

    def exit(self, *args):
        App.get_running_app().stop()

    def ready_check(self, args):
        self.label.text_source = _("Checking for readiness, do not shutdown or restart your computer or disconnect.")
        if self.firmware_api.is_ready():
            Logger.info("Printer is ready")
            self.label.text_source = _("Updating, do not shutdown or restart your computer or disconnect.")
            self.firmware_api.update_firmware(self.complete_call_back)
        else:
            Logger.info("Printer is not ready, checking again.")
            Clock.schedule_once(self.ready_check, self.check_rate)

    def complete_call_back(self, status):
        if status:
            self.image.anim_delay = -1
            self.label.text_source = _("Firmware update successful, please disconnect and reconnect your printer.")

        else:
            self.image.anim_delay = -1
            self.label.text_source = _("Firmware update failed, please disconnect the printer restart the software and try again.")
            self._complete_button.on_release = self.exit

        self.window.add_widget(self._complete_button)

    def on_leave(self):
        self.image.anim_delay = -1
