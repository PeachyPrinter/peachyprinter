import kivy
from kivy.app import App
from kivy.uix.settings import SettingsWithSidebar
from kivy.properties import StringProperty
from infrastructure.langtools import _

kivy.require('1.8.0')


class PeachyPrinter(App):
    lang = StringProperty('en_GB')

    def build(self):
        self.settings_cls = SettingsWithSidebar

    def build_settings(self, settings):
        self.settings = settings

    def on_lang(self, instance, lang):
        _.switch_lang(lang)
        if hasattr(self, 'settings'):
            self.settings.interface.menu.close_button.text = _("Close")

if __name__ == '__main__':
    PeachyPrinter().run()
