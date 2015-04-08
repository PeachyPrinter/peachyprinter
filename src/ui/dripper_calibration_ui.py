from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.clock import Clock

from kivy.logger import Logger


Builder.load_file('ui/dripper_calibration_ui.kv')


class DripperCalibrationUI(Screen):
    total_height = StringProperty('100')
    drips_per_mm = StringProperty('1.0')
    drips = StringProperty('0.0')

    def __init__(self, api, **kwargs):
        super(DripperCalibrationUI, self).__init__(**kwargs)

    def update_total_height(self):
        self.total_height = str(float(self.ids.end_height.text) - float(self.ids.start_height.text))
        self.update_drips_per_mm()

    def update_drips_per_mm(self):
        self.drips_per_mm = str(float(self.drips) / float(self.total_height))

    def on_drips(Self, instance, value):
        self.update_drips_per_mm()
