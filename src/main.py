import kivy
from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.properties import StringProperty
from infrastructure.langtools import _
from infrastructure.setting_mapper import SettingsMapper
# from peachyprinter import PrinterAPI


kivy.require('1.8.0')


class PeachyPrinter(App):
    lang = StringProperty('en_GB')

    def __init__(self, **kwargs):
        self.setting_translation = SettingsMapper()
        super(PeachyPrinter, self).__init__(**kwargs)

    def build(self):
        self.settings_cls = SettingsWithSidebar
        # self.api = PrinterAPI()

    def build_config(self, config):
        self.setting_translation.set_defaults(config)

    def build_settings(self, settings):
        self.setting_translation.refresh_settings(settings, self.config)

    def on_lang(self, instance, lang):
        _.switch_lang(lang)
        if hasattr(self, 'settings'):
            self.settings.interface.menu.close_button.text = _("Close")

if __name__ == '__main__':
    PeachyPrinter().run()
