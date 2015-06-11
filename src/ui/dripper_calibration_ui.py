from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import NumericProperty, BoundedNumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.app import App

from kivy.logger import Logger
from ui.peachy_widgets import Dripper
from ui.custom_widgets import ErrorPopup
from infrastructure.langtools import _

Builder.load_file('ui/dripper_calibration_ui.kv')


class DripperCalibrationUI(Screen):

    def __init__(self, api, **kwargs):
        self.is_active = False
        self.api = api
        self.configuration_api = None
        super(DripperCalibrationUI, self).__init__(**kwargs)
        self.circut_settings = CircutSettings()
        self.circut_settings.bind(drips_per_mm=self.drips_per_mm)
        self.emulated_settings = EmulatedSettings()
        self.emulated_settings.bind(drips_per_mm=self.drips_per_mm, drips_per_second=self.drips_per_second)
        self.photo_settings = PhotoSettings()
        self.photo_settings.bind(photo_zaxis_delay=self.photo_zaxis_delay)

    def dripper_type_changed(self, instance, value):
        Logger.info("Drippper Type change to %s" % value)
        self.ids.setup_box_id.clear_widgets()
        self.ids.visuals_box_id.clear_widgets()
        self.ids.settings_box_id.clear_widgets()

        if value == 'emulated':
            self.ids.setup_box_id.add_widget(Label(text="Emulated Setup"))
            self.ids.visuals_box_id.add_widget(Label(text="Emulated Visuals"))
            self.ids.settings_box_id.add_widget(self.emulated_settings)
        elif value == 'photo':
            self.ids.setup_box_id.add_widget(Label(text="Photo Setup"))
            self.ids.visuals_box_id.add_widget(Label(text="Photo Visuals"))
            self.ids.settings_box_id.add_widget(self.photo_settings)
        elif value == 'microcontroller':
            self.ids.setup_box_id.add_widget(Label(text="Circut Setup"))
            self.ids.visuals_box_id.add_widget(Label(text="Circut Visuals"))
            self.ids.settings_box_id.add_widget(self.circut_settings)
        self.configuration_api.set_dripper_type(value)

    def on_pre_enter(self):
        try:
            self.is_active = True
            self.configuration_api = self.api.get_configuration_api()
            dripper_type = self.configuration_api.get_dripper_type()
            self.ids.dripper_type_selector.selected = dripper_type
            self.dripper_type_changed(None, dripper_type)

            self.emulated_settings.drips_per_mm = self.configuration_api.get_dripper_drips_per_mm()
            self.circut_settings.drips_per_mm = self.configuration_api.get_dripper_drips_per_mm()
            self.photo_settings.photo_zaxis_delay = self.configuration_api.get_dripper_photo_zaxis_delay()

        except:
            ep = ErrorPopup(title=_("Error"), text=_("No Peachy Printer Detected"))
            ep.open()
            App.get_running_app().root.current = 'mainui'

    def on_pre_leave(self):
        self.is_active = False
        # self.ids.dripper_setup.clear_widgets()
        if self.configuration_api:
            self.configuration_api.stop_counting_drips()
        self.configuration_api = None

    def drips_per_mm(self, instance, value):
        Logger.info('Drips_Per_mm set to %s' % value)
        self.configuration_api.set_dripper_drips_per_mm(value)
        self.circut_settings.drips_per_mm = value
        self.emulated_settings.drips_per_mm = value

    def drips_per_second(self, instance, value):
        Logger.info('Drips_Per_Second set to %s' % value)
        self.configuration_api.set_dripper_emulated_drips_per_second(value)

    def photo_zaxis_delay(self, instance, value):
        Logger.info('photo zaxis delay set to %s' % value)
        self.configuration_api.set_dripper_photo_zaxis_delay(value)


class CircutSettings(BoxLayout):
    drips_per_mm = BoundedNumericProperty(10, min=0.0001, max=None)

class EmulatedSettings(BoxLayout):
    drips_per_second = BoundedNumericProperty(10, min=0.0001, max=None)
    drips_per_mm = BoundedNumericProperty(10, min=0.0001, max=None)

class PhotoSettings(BoxLayout):
    photo_zaxis_delay = BoundedNumericProperty(10, min=0.0001, max=None)


class MicrocontrollerDripSetup(BoxLayout):
    total_height = NumericProperty(100.0)
    drips_per_mm = NumericProperty(1.0)
    current_drips_per_mm = NumericProperty(0.0)
    drips = NumericProperty(0.0)
    average_drips = NumericProperty(0.0)

    def __init__(self, api, **kwargs):
        self.is_active = False
        self.dripper = None
        if "visualizations" in kwargs:
            self.visualizations = kwargs["visualizations"]
            self.dripper = Dripper(size_hint_x=None, width=30)
            self.visualizations.add_widget(Label())
            self.visualizations.add_widget(self.dripper)
        self.configuration_api = api
        super(MicrocontrollerDripSetup, self).__init__(**kwargs)
        Logger.info("Starting up dripper")
        self.ids.ui_drips_per_mm.text = '%.2f' % self.configuration_api.get_dripper_drips_per_mm()
        self.configuration_api.start_counting_drips(self.drip_call_back)

    def drip_call_back(self, drips, current_z_location_mm, average_drips, drip_history):
        self.drips = drips
        self.average_drips = average_drips
        if self.dripper:
            self.dripper.update_parts(drips, drip_history)

    def on_parent(self, instance, value):
        if value is None:
            Logger.info("Shutting down dripper")
            self.configuration_api.stop_counting_drips()

    def update_total_height(self):
        self.total_height = self.ids.end_height.text - self.ids.start_height.text
        self.update_drips_per_mm()

    def update_drips_per_mm(self):
        self.current_drips_per_mm = self.drips / self.total_height

    def on_drips(self, instance, value):
        self.update_drips_per_mm()

    def on_drips_per_mm(self, instance, value):
        Logger.info("Useing the drips per mm amount of %.2f" % value)
        self.ids.ui_drips_per_mm.text = '%.2f' % value
        self.configuration_api.set_dripper_drips_per_mm(value)

    def use_current(self):
        Logger.info("Useing current drips")
        self.drips_per_mm = self.current_drips_per_mm

    def reset_drip_count(self):
        self.configuration_api.reset_drips()
