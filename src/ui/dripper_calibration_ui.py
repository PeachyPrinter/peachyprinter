from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


Builder.load_file('ui/dripper_calibration_ui.kv')


class DripperCalibrationUI(Screen):
    def __init__(self, api, **kwargs):
        super(DripperCalibrationUI, self).__init__(**kwargs)
