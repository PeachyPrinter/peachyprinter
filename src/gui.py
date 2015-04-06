import os

from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

from kivy.uix.screenmanager import ScreenManager, Screen

from infrastructure.setting_mapper import SettingsMapper
from infrastructure.langtools import _
from ui.printui import PrintingUI
from ui.libraryui import LibraryUI
from ui.dripper_calibration_ui import DripperCalibrationUI
from ui.cure_test_ui import CureTestUI

from ui.custom_widgets import *


class SelectedFile(object):
    def __init__(self, path=None, filename=None):
        self.path = path
        self.filename = filename


class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)


class SettingsSelector(Popup):
    pass

class MainUI(Screen):
    setting = ObjectProperty()

    def __init__(self, selected_file, **kwargs):
        super(MainUI, self).__init__(**kwargs)
        self.selected_file = selected_file
        self.settings = SettingsSelector()

    def show_load(self):
        content = LoadDialog(load=self.load, cancel=self.dismiss_popup)
        self._popup = Popup(title=_("Load file"), content=content, size_hint=(0.9, 0.9))
        self._popup.open()

    def load(self, path, filename):
        self.selected_file.path = path
        self.selected_file.filename = filename
        self.dismiss_popup()
        self.parent.current = 'printingui'

    def dismiss_popup(self):
        self._popup.dismiss()

    def setting_selected(self):
        self.settings.open()


class MyScreenManager(ScreenManager):
    def __init__(self, api, setting_translation,  **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.api = api
        selected_file = SelectedFile()
        self.setting_translation = setting_translation
        self.main_ui = MainUI(selected_file)
        self.printing_ui = PrintingUI(self.api, selected_file)
        self.library_ui = LibraryUI(self.api)
        self.dripper_calibration_ui = DripperCalibrationUI(self.api)
        self.cure_test_ui = CureTestUI()
        self.add_widget(self.main_ui)
        self.add_widget(self.printing_ui)
        self.add_widget(self.library_ui)
        self.add_widget(self.dripper_calibration_ui)
        self.add_widget(self.cure_test_ui)


class PeachyPrinter(App):
    lang = StringProperty('en_GB')

    def __init__(self, api, **kwargs):
        self.api = api
        self.setting_translation = SettingsMapper(self.api)
        super(PeachyPrinter, self).__init__(**kwargs)
        self.manager = None

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.setting_translation.load_config(self.config)
        self.config.add_callback(self.setting_translation.update_setting)
        self.manager = MyScreenManager(self.api, self.setting_translation)
        return self.manager

    def build_config(self, config):
        self.setting_translation.set_defaults(config)

    def build_settings(self, settings):
        self.setting_translation.refresh_settings(settings, self.config)

    def on_lang(self, instance, lang):
        _.switch_lang(lang)
        self.destroy_settings()
        if hasattr(self, 'settings'):
            self.settings.interface.menu.close_button.text = _("Close")

    def on_stop(self):
        if self.manager:
            self.manager.current = 'mainui'
