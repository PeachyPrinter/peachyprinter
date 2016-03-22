
from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.config import Config
from kivy.resources import resource_add_path, resource_find
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.logger import Logger
from kivy.loader import Loader

from infrastructure.setting_mapper import SettingsMapper
from infrastructure.langtools import _

from ui.print_ui import PrintingUI
from ui.library_ui import LibraryUI
from ui.firmware_ui import FirmwareUI, FirmwareUpdateUI
from ui.dripper_calibration_ui import DripperCalibrationUI
from ui.cure_test_ui import CureTestUI
from ui.calibrate_ui import CalibrateUI
from ui.restore_ui import RestoreUI
from ui.custom_widgets import *
from peachyprinter import MissingPrinterException
import peachyprinter


import os
from os.path import join, dirname
import locale
import gettext


class LoadDialog(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    last_directory = StringProperty('~')


class SettingsSelector(I18NPopup):
    pass


class LastPrint(object):
    def __init__(self):
        self.print_type = None
        self.source = None

    def set(self, print_type, source):
        self.print_type = print_type
        self.source = source
        Logger.info("Last print was from: %s with %s" % (self.print_type, str(self.source)))


class Disclaimer(BoxLayout):
    def __init__(self, accept, reject, **kwargs):
        self.accept = accept
        self.reject = reject
        super(Disclaimer, self).__init__(**kwargs)


class MainUI(Screen):
    setting = ObjectProperty()
    last_directory = StringProperty('~')
    api_version = StringProperty("")
    ui_version = StringProperty("")
    lib_version = StringProperty("")

    def __init__(self, **kwargs):
        super(MainUI, self).__init__(**kwargs)
        self.settings = SettingsSelector()
        Clock.schedule_once(self.show_disclaimer)
        try:
            from UIVERSION import version as ui_version
        except:
            ui_version = "DEV"
        self.ui_version = ui_version
        self.api_version = peachyprinter.version
        self.lib_version = peachyprinter.lib_version

    def show_disclaimer(self, *args):
        accepted_disclaimer = Config.getdefault('internal', 'disclaimer', False)
        if not accepted_disclaimer:
            self._disclaimer = I18NPopup(
                title_source=_("Disclaimer"),
                content=Disclaimer(self.accept_disclaimer, self.reject_disclaimer, ),
                size_hint=(0.9, 0.9),
                auto_dismiss=False)
            self._disclaimer.open()

    def accept_disclaimer(self):
        Config.set('internal', 'disclaimer', True)
        Config.write()
        self._disclaimer.dismiss()

    def reject_disclaimer(self):
        App.get_running_app().stop()

    def show_load(self):
        self.last_directory = Config.getdefault('internal', 'last_directory', self.last_directory)
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup, last_directory=self.last_directory)
        self._popup = I18NPopup(title_source=_("Load file"), content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename, start_height):
        self.last_directory = path
        Config.set('internal', 'last_directory', self.last_directory)
        Config.write()
        self.dismiss_popup()
        App.get_running_app().last_print.set("file", filename)
        self.parent.current = 'printingui'
        self.parent.printing_ui.print_file(filename, start_height)

    def dismiss_popup(self):
        self._popup.dismiss()

    def setting_selected(self):
        self.settings.open()


class LoadingUI(Screen):
    def __init__(self, api,  **kwargs):
        super(LoadingUI, self).__init__(**kwargs)
        self.api = api

    def on_enter(self):
        self.image.anim_delay = 1 / 30.0
        Clock.schedule_once(self.attempt_connection)

    def on_leave(self):
        self.image.anim_delay = -1

    def _is_firmware_update_required(self):
        Logger.info("Checking for bootloader")
        if self.api.get_firmware_api().is_ready():
            Logger.info("Bootloader found")
            return True
        Logger.info("Loading Printer")
        self.api.load_printer()
        actual_version = self.api.get_configuration_api().get_info_firmware_version_number()
        Logger.info("Got Printer Firmware Version: {}".format(actual_version))
        return not self.api.get_firmware_api().is_firmware_valid(actual_version)

    def attempt_connection(self, *args):
        try:
            firmware_required = self._is_firmware_update_required()
            if firmware_required:
                Logger.info("Printer Connection Complete")
                self.parent.firmware_required()
            else:
                Logger.info("Printer Connection Complete")
                self.parent.connected()
        except MissingPrinterException:
            Logger.info("Printer not found checking again")
            Clock.schedule_once(self.attempt_connection, 2)
        except Exception as ex:
            Logger.error(ex.message)
            raise


class ExitUI(Screen):
    pass


class MyScreenManager(ScreenManager):
    def __init__(self, api, setting_translation,  **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.setting_translation = setting_translation
        self.api = api
        self.loading_ui = LoadingUI(self.api)
        self.add_widget(self.loading_ui)
        self.exit_ui = ExitUI()
        self.add_widget(self.exit_ui)

    def firmware_required(self):
        self.firmware_ui = FirmwareUI(self.api)
        self.add_widget(self.firmware_ui)
        self.firmware_update_ui = FirmwareUpdateUI(self.api)
        self.add_widget(self.firmware_update_ui)
        self.current = 'firmware_ui'

    def connected(self):
        App.get_running_app().connect_to_printer()
        self.main_ui = MainUI()

        self.firmware_update_ui = FirmwareUpdateUI(self.api)
        self.printing_ui = PrintingUI(self.api)
        self.library_ui = LibraryUI(self.api)
        self.dripper_calibration_ui = DripperCalibrationUI(self.api)
        self.calibration_ui = CalibrateUI(self.api)
        self.cure_test_ui = CureTestUI(self.api)
        self.restore_ui = RestoreUI(self.api)

        self.add_widget(self.main_ui)
        self.add_widget(self.printing_ui)
        self.add_widget(self.library_ui)
        self.add_widget(self.dripper_calibration_ui)
        self.add_widget(self.cure_test_ui)
        self.add_widget(self.calibration_ui)
        self.add_widget(self.restore_ui)

        self.current = 'main_ui'


class PeachyPrinter(App):
    large_button_height = NumericProperty(dp(52))
    button_height = NumericProperty(dp(40))
    label_height = NumericProperty(dp(30))
    input_height = NumericProperty(dp(30))
    refresh_rate = NumericProperty(1.0 / 30.0)
    use_kivy_settings = False
    lang = StringProperty('en_GB')
    translator = ObjectProperty(None, allownone=True)
    supported_languages = ['en_GB', 'en_US', 'tlh']

    def __init__(self, api, language=None, **kwargs):
        resource_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'resources')
        resource_add_path(resource_path)
        resource_add_path(os.path.join(resource_path, 'objects'))
        resource_add_path(os.path.join(resource_path, 'shaders'))
        resource_add_path(os.path.join(resource_path, 'images'))
        self.last_print = LastPrint()
        self.api = api
        self.setting_translation = SettingsMapper(self.api)
        if language:
            lang = language
        else:
            lang = locale.getdefaultlocale()[0]
        Logger.info("Specifed Language Locale: %s" % lang)
        if lang not in self.supported_languages:
            lang = 'en_GB'
        Window.size = (1000, 700)
        Window.minimum_width = 1000
        Window.minimum_height = 700
        super(PeachyPrinter, self).__init__(**kwargs)
        self.lang = lang
        Config.set("input", "mouse", "mouse,disable_multitouch")
        Config.set("kivy", "exit_on_escape", 0)
        Config.adddefaultsection('internal')
        self.switch_lang(self.lang)
        self.manager = None

    def translation(self, text):
        if text:
            translated = self.translator(text)
        else:
            translated = ""
        Logger.debug("Translating '%s' -> '%s'" % (text, translated))
        return translated

    def on_lang(self, instance, lang):
        self.switch_lang(lang)

    def open_settings(self):
        self.destroy_settings()
        super(PeachyPrinter, self).open_settings()

    def switch_lang(self, lang):
        Logger.info("Using Language Locale: %s" % self.lang)
        locale_dir = join(dirname(__file__), 'resources', 'il8n', 'locales')
        locales = gettext.translation('peachyprinter', locale_dir, languages=[self.lang])
        self.translator = locales.ugettext
        if hasattr(self, 'settings'):
            self.settings.interface.menu.close_button.text = self.translation(_("Close"))

    def exit_app(self, *args):
        self.stop()

    def build(self):
        self.icon = os.path.join(os.path.dirname(__file__), 'resources', 'peachy.png')
        self.settings_cls = SettingsWithSidebar
        self.manager = MyScreenManager(self.api, self.setting_translation)
        return self.manager

    def connect_to_printer(self):
        try:
            self.setting_translation.load_config(self.config)
            self.config.add_callback(self.setting_translation.update_setting)
            self.api.get_configuration_api().get_current_config()
            return True
        except MissingPrinterException:
            return False
        except Exception as ex:
            fail_box = BoxLayout(orientation="vertical")
            pop_message = I18NLabel(text_source=_("An Error has Occured"), size_hint_y=None, height=self.label_height,)
            pop_error = I18NLabel(text_source=str(ex))
            pop_exit = I18NButton(text_source=_("Exit"), size_hint_y=None, height=self.button_height, on_release=self.exit_app)
            fail_box.add_widget(pop_message)
            fail_box.add_widget(pop_error)
            fail_box.add_widget(pop_exit)
            return fail_box

    def build_config(self, config):
        self.setting_translation.set_defaults(config)

    def build_settings(self, settings):
        self.setting_translation.refresh_settings(settings, self.config)
        settings.interface.menu.close_button.text = self.translation(_("Close"))

    def on_stop(self):
        if self.manager:
            self.manager.current = 'exit_ui'
