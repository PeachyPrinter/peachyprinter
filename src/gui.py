from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.properties import StringProperty
from kivy.uix.floatlayout import FloatLayout

from kivy.uix.screenmanager import ScreenManager, Screen

from infrastructure.setting_mapper import SettingsMapper
from infrastructure.langtools import _
from ui.printui import PrintingUI

from ui.custom_widgets import *


class MainUI(Screen):
    pass


class MyScreenManager(ScreenManager):
    def __init__(self, api, setting_translation,  **kwargs):
        super(MyScreenManager, self).__init__(**kwargs)
        self.api = api
        self.setting_translation = setting_translation
        self.printing_ui = PrintingUI(self.api)
        self.add_widget(self.printing_ui)


class PeachyPrinter(App):
    lang = StringProperty('en_GB')

    def __init__(self, api, **kwargs):
        self.api = api
        self.setting_translation = SettingsMapper(self.api)
        super(PeachyPrinter, self).__init__(**kwargs)

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.setting_translation.load_config(self.config)
        self.config.add_callback(self.setting_translation.update_setting)
        return MyScreenManager(self.api, self.setting_translation)

    def build_config(self, config):
        self.setting_translation.set_defaults(config)

    def build_settings(self, settings):
        self.setting_translation.refresh_settings(settings, self.config)

    def on_lang(self, instance, lang):
        _.switch_lang(lang)
        self.destroy_settings()
        if hasattr(self, 'settings'):
            self.settings.interface.menu.close_button.text = _("Close")
