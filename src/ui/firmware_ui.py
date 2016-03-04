from kivy.uix.screenmanager import Screen
from kivy.logger import Logger
from kivy.lang import Builder
from ui.custom_widgets import I18NButton
from kivy.app import App

from kivy.clock import Clock

from infrastructure.langtools import _
from ui.custom_widgets import I18NPopup


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
            version = self.api.get_configuration_api().get_info_firmware_version_number()
        except:
            Logger.info("Could not get printer information for firmware version check")
            version = ''
        self.actual_version = self._get_display_version(version)

    def _get_display_version(self, reported_version):
            if self.firmware_api.is_ready():
                return _('Bootloader')
            elif reported_version == '':
                return self._bootloader_required()
            elif self._get_revision_from_verison(reported_version) < 238:
                return self._bootloader_required()
            else:
                return reported_version

    def _bootloader_required(self):
        self.update_button.parent.remove_widget(self.update_button)
        FirmwareManualBootloaderPopup().open()
        return _('Unsupported')

    def _get_revision_from_verison(self, version):
        try:
            return int(version.split('.')[-1])
        except:
            return 0

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
        self._complete_button = I18NButton(text_source=_("Continue"), on_release=self.close, size_hint_y=None, height=app.button_height)

    def on_enter(self):
        self.image.anim_delay = 1.0 / 30.0
        self.firmware_api = self.api.get_firmware_api()
        Clock.schedule_once(self.ready_check, self.check_rate)

    def close(self, *args):
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
            Clock.schedule_once(self._complete_success)
        else:
            Clock.schedule_once(self._complete_fail)

    def _complete_fail(self, *args):
        self.image.anim_delay = -1
        self.label.text_source = _("Firmware update failed, please disconnect the printer restart the software and try again.")
        self._complete_button.on_release = self.exit
        self.window.add_widget(self._complete_button)

    def _complete_success(self, *args):
        self.label.text_source = _("Firmware update successful. Please disconnect and reconnect your printer.")
        self.image.source = 'resources/images/firmware_out_in_512x512.zip'
        self.image.anim_delay = 1.0 / 15.0
        Clock.schedule_once(self._check_for_peachy, 0.5)

    def _check_for_peachy(self, *args):
        try:
            Logger.info("Get current firmware")

            self.api.load_printer()
            self.api.get_configuration_api().get_info_firmware_version_number()

            self.image.anim_delay = -1
            self.close()
        except:
            Logger.info("Could not get printer information for firmware version check")
            Clock.schedule_once(self._check_for_peachy, 0.5)

    def on_leave(self):
        self.image.anim_delay = -1


class FirmwareManualBootloaderPopup(I18NPopup):
    pass