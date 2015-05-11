from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.app import App

from kivy.logger import Logger
from ui.peachy_widgets import Dripper
from ui.custom_widgets import ErrorPopup
from infrastructure.langtools import _

Builder.load_file('ui/dripper_calibration_ui.kv')


class I18NKeyedSpinner(Spinner):
    keys = ListProperty()
    key = StringProperty()
    text_source = StringProperty('')
    values_source = ListProperty()

    def on_text(self, instance, value):
        print(self.values)
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
        self.ids.visualizations.clear_widgets()

        if value == 'emulated':
            self.ids.dripper_setup.add_widget(EmulatedDripSetup(self.configuration_api))
        elif value == 'photo':
            self.ids.dripper_setup.add_widget(PhotoDripSetup(self.configuration_api))
        elif value == 'microcontroller':
            self.ids.dripper_setup.add_widget(MicrocontrollerDripSetup(self.configuration_api, visualizations=self.ids.visualizations))


        self.configuration_api.set_dripper_type(value)

    def on_pre_enter(self):
        try:
            self.is_active = True
            self.configuration_api = self.api.get_configuration_api()
            dripper_type = self.configuration_api.get_dripper_type()
            self.ids.dripper_type_selector.key = dripper_type
            self.dripper_type_changed(None, dripper_type)
        except:
            ep = ErrorPopup(title=_("Error"), text=_("No Peachy Printer Detected"))
            ep.open()
            App.get_running_app().root.current = 'mainui'

    def on_pre_leave(self):
        self.is_active = False
        self.ids.dripper_setup.clear_widgets()
        if self.configuration_api:
            self.configuration_api.stop_counting_drips()
        self.configuration_api = None


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
