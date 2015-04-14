from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.spinner import Spinner
from kivy.clock import Clock

from kivy.logger import Logger


Builder.load_file('ui/dripper_calibration_ui.kv')


class KeyedSpinner(Spinner):
    keys = ListProperty()
    key = StringProperty()

    def on_text(self, instance, value):
        idx = self.values.index(value)
        self.key = self.keys[idx]

    def on_key(self, instance, key):
        idx = self.keys.index(key)
        self.text = self.values[idx]

class DripperCalibrationUI(Screen):

    def __init__(self, api, **kwargs):
        self.is_active = False
        self.api = api
        self.configuration_api = None
        super(DripperCalibrationUI, self).__init__(**kwargs)

    def dripper_type_changed(self, instance, value):
        Logger.info("Drippper Type change to %s" % value)
        self.ids.dripper_setup.clear_widgets()

        if value == 'emulated':
            self.ids.dripper_setup.add_widget(EmulatedDripSetup(self.configuration_api))
        elif value == 'photo':
            self.ids.dripper_setup.add_widget(PhotoDripSetup(self.configuration_api))
        elif value =='microcontroller':
            self.ids.dripper_setup.add_widget(MicrocontrollerDripSetup(self.configuration_api))

        self.configuration_api.set_dripper_type(value)

    def on_pre_enter(self):
        self.is_active = True
        self.configuration_api = self.api.get_configuration_api()
        dripper_type = self.configuration_api.get_dripper_type()
        self.ids.dripper_type_selector.key = dripper_type
        self.dripper_type_changed(None, dripper_type)


    def on_pre_leave(self):
        self.is_active = False
        if self.configuration_api:
            self.configuration_api.stop_counting_drips()
        self.configuration_api = None


# set_dripper_drips_per_mm
# set_dripper_type
# set_dripper_emulated_drips_per_second
# set_dripper_photo_zaxis_delay


class EmulatedDripSetup(BoxLayout):
    drips_per_second = NumericProperty()
    drips_per_mm = NumericProperty()

    def __init__(self, configuration_api, **kwargs):
        self.is_active = False
        self.configuration_api = configuration_api
        self.drips_per_second = self.configuration_api.get_dripper_emulated_drips_per_second()
        self.drips_per_mm = self.configuration_api.get_dripper_drips_per_mm()
        super(EmulatedDripSetup, self).__init__(**kwargs)

    def on_drips_per_second(self, instance, value):
        Logger.info('Drips_Per_Second set to %s' % value)
        self.configuration_api.set_dripper_emulated_drips_per_second(value)

    def on_drips_per_mm(self, instance, value):
        Logger.info('Drips_Per_mm set to %s' % value)
        self.configuration_api.set_dripper_drips_per_mm(value)


class PhotoDripSetup(BoxLayout):
    photo_zaxis_delay = NumericProperty()

    def __init__(self, configuration_api, **kwargs):
        self.is_active = False
        self.configuration_api = configuration_api
        self.photo_zaxis_delay = self.configuration_api.get_dripper_photo_zaxis_delay()
        super(PhotoDripSetup, self).__init__(**kwargs)

    def on_photo_zaxis_delay(self, instance, value):
        Logger.info('photo zaxis delay set to %s' % value)
        self.configuration_api.set_dripper_photo_zaxis_delay(value)

class MicrocontrollerDripSetup(BoxLayout):
    total_height = NumericProperty(100)
    drips_per_mm = NumericProperty(1.0)
    drips = NumericProperty(0.0)

    def __init__(self, api, **kwargs):
        self.is_active = False
        self.configuration_api = api
        super(MicrocontrollerDripSetup, self).__init__(**kwargs)

    def update_total_height(self):
        self.total_height = self.ids.end_height.text - self.ids.start_height.text
        self.update_drips_per_mm()

    def update_drips_per_mm(self):
        self.drips_per_mm = self.drips / self.total_height

    def on_drips(self, instance, value):
        self.update_drips_per_mm()