
from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.config import Config
from infrastructure.setting_mapper import SettingsMapper
from infrastructure.langtools import _

from ui.print_ui import PrintingUI
from ui.library_ui import LibraryUI
from ui.dripper_calibration_ui import DripperCalibrationUI
from ui.cure_test_ui import CureTestUI
from ui.calibrate_ui import CalibrateUI
from ui.restore_ui import RestoreUI
from ui.custom_widgets import *
from peachyprinter import MissingPrinterException


from os.path import join, dirname
import gettext


class LoadDialog(BoxLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    last_directory = StringProperty('~')


class SettingsSelector(I18NPopup):
    pass


class MainUI(Screen):
    setting = ObjectProperty()
    last_directory = StringProperty('~')

    def __init__(self, **kwargs):
        super(MainUI, self).__init__(**kwargs)
        self.settings = SettingsSelector()

    def show_load(self):
        Config.adddefaultsection('internal')
        self.last_directory = Config.getdefault('internal', 'last_directory', self.last_directory)
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup, last_directory=self.last_directory)
        self._popup = I18NPopup(title_source=_("Load file"), content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.last_directory = path
        Config.set('internal', 'last_directory', self.last_directory)
        Config.write()
        self.dismiss_popup()
        self.parent.current = 'printingui'
        self.parent.printing_ui.print_file(filename)

    def dismiss_popup(self):
        self._popup.dismiss()

    def setting_selected(self):
        self.settings.open()


class MyScreenManager(ScreenManager):
    def __init__(self, api, setting_translation,  **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.api = api
        self.setting_translation = setting_translation
        self.main_ui = MainUI()
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


class PeachyPrinter(App):
    lang = StringProperty('en_GB')
    translator = ObjectProperty(None, allownone=True)

    def __init__(self, api, language=None, **kwargs):
        self.api = api
        self.setting_translation = SettingsMapper(self.api)
        super(PeachyPrinter, self).__init__(**kwargs)
        Config.set("input", "mouse", "mouse,disable_multitouch")
        if language:
            self.lang = language
        self.switch_lang(self.lang)
        self.manager = None

    def translation(self, text):
        if text:
            translated = self.translator(text)
        else:
            translated = ""
        Logger.info("Translating '%s' -> '%s'" % (text, translated))
        return translated

    def on_lang(self, instance, lang):
        self.switch_lang(lang)

    def open_settings(self):
        self.destroy_settings()
        super(PeachyPrinter, self).open_settings()

    def switch_lang(self, lang):
        locale_dir = join(dirname(__file__), 'resources', 'il8n', 'locales')
        locales = gettext.translation('peachyprinter', locale_dir, languages=[self.lang])
        self.translator = locales.ugettext
        if hasattr(self, 'settings'):
            self.settings.interface.menu.close_button.text = self.translation(_("Close"))

    def build(self):
        self.settings_cls = SettingsWithSidebar
        try:
            self.setting_translation.load_config(self.config)
            self.config.add_callback(self.setting_translation.update_setting)
        except MissingPrinterException:
            fail_box = BoxLayout(orientation="vertical")
            pop_message = I18NLabel(text_source=_("Please connect your peachy printer before starting the software"))
            pop_exit = I18NButton(text_source=_("Exit"), size_hint_y = None, height=30, on_release=exit)
            fail_box.add_widget(pop_message)
            fail_box.add_widget(pop_exit)
            return fail_box
        self.manager = MyScreenManager(self.api, self.setting_translation)
        return self.manager

    def build_config(self, config):
        self.setting_translation.set_defaults(config)

    def build_settings(self, settings):
        self.setting_translation.refresh_settings(settings, self.config)
        settings.interface.menu.close_button.text = self.translation(_("Close"))

    def on_stop(self):
        if self.manager:
            self.manager.current = 'mainui'
