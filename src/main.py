import json

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.uix.popup import Popup
from kivy.graphics.vertex_instructions import Rectangle, Ellipse, Line
from kivy.graphics.context_instructions import Color


from setting_adapter import SettingsAdapter

class Interface(BoxLayout):
    pass

class ConfigPopUp(Popup):
    pass

class SettingsApp(App):
    def __init__(self,):
        self.settings_adapter = SettingsAdapter()
        super(SettingsApp, self).__init__()

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        self.interface = Interface()
        return self.interface

    def build_config(self, config):
        for (key, value) in self.settings_adapter.defaults().items():
            config.setdefaults(key, value)

    def build_settings(self, settings):
        settings.add_json_panel("Peachy Printer", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Main']))
        settings.add_json_panel("Audio Settings", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Audio']))
        settings.add_json_panel("Advanced Options", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Options']))
        # settings.add_json_panel("Dripper Setup", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Dripper']))
        # settings.add_json_panel("Calibration Data", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Calibration']))
        settings.add_json_panel("Email Setup", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Email']))
        settings.add_json_panel("Serial Setup", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Serial']))
        settings.add_json_panel("Circut Selection", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Circut']))
        settings.add_json_panel("Micro Controller Setup", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Micro Controller']))

    def on_config_changed(self, config, section, key, value):
        print key, value

    def on_open_config(self, **kwargs):
        self.pop_up = ConfigPopUp()
        self.pop_up.open()

    def on_close_config(self, **kwargs):
        self.pop_up.dismiss()


if __name__ == '__main__':
    SettingsApp().run()