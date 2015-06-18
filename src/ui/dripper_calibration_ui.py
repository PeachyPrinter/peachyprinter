from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import NumericProperty, BoundedNumericProperty, StringProperty, ListProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.label import Label
from kivy.core.image import Image as CoreImage
from kivy.graphics import *
from kivy.clock import Clock

from kivy.app import App
from kivy.logger import Logger

import time

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
        self.circut_visuals = CircutVisuals()
        self.circut_visuals.bind(drips_per_mm=self.drips_per_mm, reset=self.reset_drip_count)
        self.circut_setup = CircutSetup()
        self.circut_setup.bind(test_height=self.test_height)

        self.emulated_settings = EmulatedSettings()
        self.emulated_settings.bind(drips_per_mm=self.drips_per_mm, drips_per_second=self.drips_per_second)
        self.emulated_visuals = EmulatedVisuals()

        self.photo_settings = PhotoSettings()
        self.photo_settings.bind(photo_zaxis_delay=self.photo_zaxis_delay)
        self.photo_visuals = PhotoVisuals()

    def dripper_type_changed(self, instance, value):
        Logger.info("Drippper Type change to %s" % value)
        self.ids.setup_box_id.clear_widgets()
        self.ids.visuals_box_id.clear_widgets()
        self.ids.settings_box_id.clear_widgets()
        self.configuration_api.stop_counting_drips()
        self.configuration_api.set_dripper_type(value)
        self.circut_visuals.stop_animation()

        if value == 'emulated':
            self.ids.setup_box_id.add_widget(BoxLayout())
            self.ids.visuals_box_id.add_widget(self.emulated_visuals)
            self.ids.settings_box_id.add_widget(self.emulated_settings)
        elif value == 'photo':
            self.ids.setup_box_id.add_widget(BoxLayout())
            self.ids.visuals_box_id.add_widget(self.photo_visuals)
            self.ids.settings_box_id.add_widget(self.photo_settings)

        elif value == 'microcontroller':
            self.ids.setup_box_id.add_widget(self.circut_setup)
            self.ids.visuals_box_id.add_widget(self.circut_visuals)
            self.circut_visuals.start_animation()
            self.ids.settings_box_id.add_widget(self.circut_settings)
            self.configuration_api.start_counting_drips(self.drip_call_back)

    def on_pre_enter(self):
        try:
            self.is_active = True
            self.configuration_api = self.api.get_configuration_api()
            dripper_type = self.configuration_api.get_dripper_type()
            self.ids.dripper_type_selector.selected = dripper_type
            self.dripper_type_changed(None, dripper_type)

            self.emulated_settings.drips_per_mm = self.configuration_api.get_dripper_drips_per_mm()
            self.circut_settings.drips_per_mm = self.configuration_api.get_dripper_drips_per_mm()
            self.circut_visuals.target_height = str(self.circut_setup.test_height)
            self.photo_settings.photo_zaxis_delay = self.configuration_api.get_dripper_photo_zaxis_delay()

        except:
            raise
            ep = ErrorPopup(title=_("Error"), text=_("No Peachy Printer Detected"))
            ep.open()
            App.get_running_app().root.current = 'mainui'

    def drip_call_back(self, drips, current_z_location_mm, average_drips, drip_history):
        self.circut_visuals.drips = str(drips)
        self.circut_visuals.average_drips = "{:.2f}".format(average_drips)
        self.circut_visuals.drip_history = drip_history

    def on_pre_leave(self):
        self.is_active = False
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

    def test_height(self, instance, value):
        Logger.info('Drip test height set to %s' % value)
        self.circut_visuals.target_height = str(value)

    def reset_drip_count(self, instance, value):
        self.configuration_api.reset_drips()


class CircutSetup(BoxLayout):
    test_height = BoundedNumericProperty(50)


class CircutVisuals(BoxLayout):
    drips_display = StringProperty("0")
    average_drips_display = StringProperty("0.00")
    target_height = StringProperty("0")
    drip_history_display = ListProperty()
    drips_per_mm = NumericProperty()
    reset = BooleanProperty()
    
    def __init__(self, **kwargs):
        super(CircutVisuals, self).__init__(**kwargs)
        self.drips = 0
        self.average_drips = 0
        self.drip_history = []
        self._refresh_rate = App.get_running_app().refresh_rate

    def redraw(self, *args):
        self. drips_display = self.drips
        self. average_drips_display = self.average_drips
        self. drip_history_display = self.drip_history
        Clock.schedule_once(self.redraw, self._refresh_rate)

    def calculate_drips_per_mm(self):
        self.drips_per_mm = float(self.drips) / float(self.target_height)

    def on_target_height(self, instance, value):
        self.ids.dripper_animation.test_height = float(value)

    def on_drip_history_display(self, instance,value):
        self.ids.dripper_animation.drip_history = value

    def start_animation(self):
        Clock.schedule_once(self.redraw)
        Clock.schedule_once(self.ids.dripper_animation.redraw)

    def stop_animation(self):
        Clock.unschedule(self.redraw)
        Clock.unschedule(self.ids.dripper_animation.redraw)


class DripperAnimation(RelativeLayout):
    cup_width = NumericProperty()
    cup_top = NumericProperty()
    cup_bottom = NumericProperty()
    cup_height = NumericProperty()
    cup_water_level = NumericProperty()
    cup_left = NumericProperty()
    cup_right = NumericProperty()
    cup_dest_water_level = NumericProperty()
    test_height = NumericProperty()
    drips_bottom = NumericProperty()
    drips_height = NumericProperty()
    drip_history = ListProperty()

    def __init__(self, **kwargs):
        super(DripperAnimation, self).__init__(**kwargs)
        self.drip_time_range = 5
        self._gl_setup()
        self._refresh_rate = App.get_running_app().refresh_rate

    def _gl_setup(self):
        self.drip_texture = CoreImage("resources/images/drop.png", mipmap=True).texture
        self.drips_instruction = InstructionGroup()
        self.canvas.add(self.drips_instruction)

    def redraw(self, key):
        self._draw_drips()
        Clock.unschedule(self.redraw)
        Clock.schedule_once(self.redraw, self._refresh_rate)

    def _draw_drips(self):
        self.drips_instruction.clear()
        top = time.time()
        bottom = top - self.drip_time_range
        for drip_time in self.drip_history:
            if drip_time > bottom:
                time_ago = top - drip_time
                y_pos_percent = (self.drip_time_range - time_ago) / self.drip_time_range
                drip_pos_y = self.drips_height * y_pos_percent + self.cup_water_level
                self.drips_instruction.add(Rectangle(size=[12, 16], pos=[self.dripper_left, drip_pos_y], texture= self.drip_texture))



class CircutSettings(BoxLayout):
    drips_per_mm = BoundedNumericProperty(10, min=0.0, max=None)


class EmulatedSettings(BoxLayout):
    drips_per_second = BoundedNumericProperty(10, min=0.0001, max=None)
    drips_per_mm = BoundedNumericProperty(10, min=0.0001, max=None)


class PhotoSettings(BoxLayout):
    photo_zaxis_delay = BoundedNumericProperty(10, min=0.0001, max=None)


class EmulatedVisuals(BoxLayout):
    pass


class PhotoVisuals(BoxLayout):
    pass
