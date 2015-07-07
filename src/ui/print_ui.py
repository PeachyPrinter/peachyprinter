import datetime
import time

from kivy.uix.screenmanager import Screen
from kivy.graphics import *
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty, BoundedNumericProperty
from kivy.clock import Clock
from kivy.graphics import InstructionGroup
from kivy.core.image import Image as CoreImage

from ui.custom_widgets import ErrorPopup, I18NPopup
from ui.peachy_widgets import LaserWarningPopup
from infrastructure.langtools import _
import math

import os

Builder.load_file('ui/print_ui.kv')


class ListElement(BoxLayout):
    title = StringProperty()
    value = StringProperty()


class DripSpeed(GridLayout):
    drips_per_second = BoundedNumericProperty(1.0, min=0.0, max=20.0)

    def __init__(self, set_drips_per_second, **kwargs):
        super(DripSpeed, self).__init__(**kwargs)
        self._set_drips_per_second = set_drips_per_second

    def on_drips_per_second(self, instance, value):
        self._set_drips_per_second(value)


class PrinterAnimation(RelativeLayout):
    padding = NumericProperty(40)

    printer_actual_dimensions = ListProperty([10, 10, 80])
    printer_current_actual_height = NumericProperty(0.0)

    print_area_height = NumericProperty(1)
    print_area_width = NumericProperty(1)
    print_area_left = NumericProperty(0)
    print_area_bottom = NumericProperty(40)

    container_padding = NumericProperty(0)
    container_left = NumericProperty(0)
    container_width = NumericProperty(0)
    container_bottom = NumericProperty(0)
    container_height = NumericProperty(0)

    laser_size = ListProperty([40, 40])

    resin_height = NumericProperty(20)
    water_height = NumericProperty(20)

    scale = NumericProperty(1.0)

    resin_color = ListProperty([0.0, 0.8, 0.0, 0.6])
    water_color = ListProperty([0.2, 0.2, 1.0, 0.6])
    container_color = ListProperty([1.0, 1.0, 1.0, 1.0])
    laser_color_edge2 = ListProperty([0.0, 0.0, 0.5, 1.0])
    laser_color_edge = ListProperty([0.0, 0.0, 1.0, 1.0])
    laser_color = ListProperty([0.7, 1.0, 1.0, 1.0])

    drip_history = ListProperty()
    laser_points = ListProperty()

    middle_x = NumericProperty(52)

    laser_pos = NumericProperty(60)
    laser_speed = NumericProperty(1)
    refresh_rate = NumericProperty(1.0 / 60.0)

    def __init__(self, **kwargs):
        super(PrinterAnimation, self).__init__(**kwargs)
        self.drip_time_range = 5
        self.waiting_for_drips = True
        self.refresh_rate = App.get_running_app().refresh_rate
        self._gl_setup()
        self.axis_history = []
        self.drips = 0

        self.line_x = []
        self.line_y = []
        self.last_height = 0.0
        self.min_height = 0.0
        self.last_x_min = 0.0
        self.last_x_max = 1.0
        self.is_on_canvas = False

    def on_printer_actual_dimensions(self, instance, value):
        self.min_height = self.printer_actual_dimensions[2] / 400.0
        self.on_size(None)

    def _gl_setup(self):
        self.drip_texture = CoreImage("resources/images/drop.png", mipmap=True).texture
        self.drips_instruction = InstructionGroup()
        self.model_instruction = InstructionGroup()
        print(self.canvas.children)
        # self.canvas.add(self.drips_instruction)
        # self.canvas.add(self.model_instruction)

    def on_size(self, *largs):
        bounds_y = (self.height * 0.7) - self.resin_height
        bounds_x = self.width - (self.padding * 2)
        printer_x = self.printer_actual_dimensions[0]
        printer_y = self.printer_actual_dimensions[2]
        self.laser_pos = self.width / 2

        self.scale = min(bounds_y / printer_y, bounds_x / printer_x)
        self.print_area_width = printer_x * self.scale
        self.print_area_height = printer_y * self.scale

    def redraw(self, key):
        self._draw_drips()
        self._draw_laser()
        self._draw_model()
        if not self.is_on_canvas:
            self.canvas.insert(4,self.drips_instruction)
            self.canvas.insert(4,self.model_instruction)
            self.is_on_canvas = True
        Clock.unschedule(self.redraw)
        Clock.schedule_once(self.redraw, self.refresh_rate)

    def animation_start(self, *args):
        Clock.unschedule(self.redraw)
        self.axis_history = []
        self.line_x = []
        self.line_y = []
        self.last_height = 0
        self.min_height = 0.0
        self.laser_points = []
        self.drip_history = []
        Clock.schedule_once(self.redraw, self.refresh_rate)

    def animation_stop(self):
        Clock.unschedule(self.redraw)
        self.axis_history = []
        self.line_x = []
        self.line_y = []
        self.last_height = 0
        self.min_height = 0.0
        self.laser_points = []
        self.drip_history = []

    def _draw_drips(self):
        self.drips_instruction.clear()
        self.drips_instruction.add(Color(1, 1, 1, 1))
        top = time.time()
        bottom = top - self.drip_time_range
        for (index, drip_time) in zip(range(len(self.drip_history), 0, -1), self.drip_history):
            if drip_time > bottom:
                time_ago = top - drip_time
                y_pos_percent = (self.drip_time_range - time_ago) / self.drip_time_range
                drip_pos_y = (self.height * y_pos_percent) + self.padding
                xoff = 10 + math.sin((len(self.drip_history) - index) / (2 * math.pi)) * 20
                self.drips_instruction.add(Rectangle(size=[12, 16], pos=[self.print_area_left + xoff, drip_pos_y], texture=self.drip_texture))

    def _draw_laser(self):
        if self.waiting_for_drips:
            self.laser_points = []
        else:
            x_min = self.print_area_left + (self.last_x_min * self.print_area_width)
            x_max = self.print_area_left + (self.last_x_max * self.print_area_width)
            if (self.laser_pos >= x_max):
                self.laser_pos = x_max
                self.laser_speed = abs(self.laser_speed) * -1
            if (self.laser_pos <= x_min):
                self.laser_pos = x_min
                self.laser_speed = abs(self.laser_speed)

            self.laser_pos += self.laser_speed
            laser_x = self.laser_pos
            self.laser_points = [self.middle_x, self.height - self.padding,
                                 laser_x,          self.water_height + self.print_area_bottom + self.resin_height]

    def _draw_model(self):
            self.model_instruction.clear()
            self.model_instruction.add(Color(rgba=(1.0,0.0,0.0,1.0)))
            if self.axis_history:
                model_height = self.axis_history[-1][2]
                if model_height > (self.last_height + self.min_height) or not self.line_x:
                    x1, y1, x2, y2 = self._get_pixels(self.axis_history[-1])
                    self.last_x_min = x1
                    self.last_x_max = x2

                    self.line_x.insert(0, x1)
                    self.line_x.append(x2)
                    self.line_y.insert(0, y1)
                    self.line_y.append(y2)
                    self.last_height = model_height

                points = []
                for idx in range(0, len(self.line_x)):
                    x = int(self.print_area_left + (self.line_x[idx] * self.print_area_width))
                    y = int(self.print_area_bottom + self.resin_height + (self.line_y[idx] * self.print_area_height)) - 2
                    points.append(x)
                    points.append(y)

                self.model_instruction.add(Line(points=points, width=2, close=True))

    def _get_pixels(self, data):
        pixel_height = data[2] / self.printer_actual_dimensions[2]
        pixel_pos_min = (data[0][0] + (self.printer_actual_dimensions[1] / 2.0)) / self.printer_actual_dimensions[1]
        pixel_pos_max = (data[0][1] + (self.printer_actual_dimensions[1] / 2.0)) / self.printer_actual_dimensions[1]
        return [pixel_pos_min, pixel_height, pixel_pos_max, pixel_height]


class SettingsPopUp(I18NPopup):
    def add_setting(self, widget):
        self.ids.print_settings.add_widget(widget)

    def remove_settings(self):
        self.ids.print_settings.clear_widgets()


class PrintingUI(Screen):
    printer_actual_dimensions = ListProperty([10, 10, 10])

    status = StringProperty("Starting")
    model_height = NumericProperty(0.0)
    start_time = ObjectProperty(datetime.datetime.now())
    drips = NumericProperty(0)
    print_height = NumericProperty(0.0)
    drips_per_second = NumericProperty(0.0)
    errors = ListProperty()
    waiting_for_drips = StringProperty("Starting")
    elapsed_time = StringProperty("0")
    current_layer = NumericProperty(0)
    skipped_layers = NumericProperty(0)

    def __init__(self, api, **kwargs):
        self.return_to = 'mainui'
        self.dripper_setting = None
        super(PrintingUI, self).__init__(**kwargs)
        self.api = api
        printer = api.get_current_config()
        self.printer_actual_dimensions = [
            printer.calibration.print_area_x,
            printer.calibration.print_area_y,
            printer.calibration.print_area_z]

        self.print_api = None
        self.print_options = []
        self.settings_popup = SettingsPopUp()
        self.refresh_rate = App.get_running_app().refresh_rate

    def on_printer_actual_dimensions(self, instance, value):
        self.ids.printer_animation.printer_actual_dimensions = value

    def on_model_height(self, instance, value):
        self.ids.printer_animation.printer_current_actual_height = value

    def time_delta_format(self, td):
        total_seconds = td.total_seconds()
        hours = int(total_seconds) / (60 * 60)
        remainder = int(total_seconds) % (60 * 60)
        minutes = remainder / 60
        return "{0}:{1:02d}".format(hours, minutes)

    def _update_status(self, arg):
        data = self.print_api.get_status()
        if 'status' in data:
            self.status = data['status']
        if 'model_height' in data:
            self.model_height = data['model_height']
        if 'start_time' in data:
            self.start_time = data['start_time']
        if 'drips' in data:
            self.drips = data['drips']
            self.ids.printer_animation.drips = data['drips']
        if 'height' in data:
            self.print_height = data['height']
        if 'drips_per_second' in data:
            self.drips_per_second = data['drips_per_second']
        if 'errors' in data:
            self.errors = data['errors']
        if 'waiting_for_drips' in data:
            self.ids.printer_animation.waiting_for_drips = data['waiting_for_drips']
            self.waiting_for_drips = str(data['waiting_for_drips'])
        if 'elapsed_time' in data:
            self.elapsed_time = self.time_delta_format(data['elapsed_time'])
        if 'current_layer' in data:
            self.current_layer = data['current_layer']
        if 'skipped_layers' in data:
            self.skipped_layers = data['skipped_layers']
        if 'drip_history' in data:
            self.ids.printer_animation.drip_history = data['drip_history']
        if 'axis' in data:
            self.ids.printer_animation.axis_history = data['axis']

        Clock.unschedule(self._update_status)
        if self.status == 'Complete':
            self.ids.printer_animation.animation_stop()
            self.play_complete_sound()
            self.ids.navigate_button.text_source = _("Print Complete")
            self.ids.navigate_button.background_color = [0.0, 2.0, 0.0, 1.0]
        elif self.status == 'Failed':
            self.ids.printer_animation.animation_stop()
            self.play_failed_sound()
            self.ids.navigate_button.text_source = _("Print Failed")
            self.ids.navigate_button.background_color = [2.0, 0.0, 0.0, 1.0]
        else:
            Clock.schedule_once(self._update_status, self.refresh_rate)

    def print_file(self, *args, **kwargs):
        self.print_options = [self._print_file, args, kwargs]
        popup = LaserWarningPopup(title=_('Laser Safety Notice'), size_hint=(0.6, 0.6))
        popup.bind(on_dismiss=self.is_safe)
        popup.open()

    def _print_file(self, filename, start_height=0.0, return_name='mainui', force_source_speed=False):
        self.return_to = return_name
        try:
            filepath = filename[0].encode('utf-8')
            self.print_api = self.api.get_print_api(start_height=start_height)
            self.path = os.path.basename(filepath)
            self.print_api.print_gcode(filepath, force_source_speed=force_source_speed)
            self.setup_dripper()
        except Exception as ex:
            popup = ErrorPopup(title='Error', text=str(ex), size_hint=(0.6, 0.6))
            popup.open()
            self.parent.current = self.return_to

    def is_safe(self, instance):
        if instance.is_safe():
            self.ids.printer_animation.axis_history = []
            Clock.schedule_once(self.ids.printer_animation.animation_start)
            Clock.schedule_once(self._update_status, self.refresh_rate)
            self.print_options[0](*self.print_options[1], **self.print_options[2])
        else:
            self.parent.current = self.return_to

    def setup_dripper(self):
        if self.print_api and self.print_api.can_set_drips_per_second():
            self.dripper_setting = DripSpeed(self.print_api.set_drips_per_second)
            self.dripper_setting.drips_per_second = self.print_api.get_drips_per_second()
            self.ids.dripper_grid.add_widget(self.dripper_setting)


    def print_generator(self, *args, **kwargs):
        self.print_options = [self._print_generator, args, kwargs]
        popup = LaserWarningPopup()
        popup.bind(on_dismiss=self.is_safe)
        popup.open()

    def _print_generator(self, generator, return_name='mainui', force_source_speed=False):
        self.return_to = return_name
        try:
            self.print_api = self.api.get_print_api()
            self.print_api.print_layers(generator, force_source_speed=force_source_speed)
            self.setup_dripper()
        except Exception as ex:
            popup = ErrorPopup(title='Error', text=str(ex), size_hint=(0.6, 0.6))
            popup.open()
            self.parent.current = self.return_to

    def restart(self):
        Clock.unschedule(self._update_status)
        self.ids.printer_animation.animation_stop()
        if self.dripper_setting:
            self.ids.dripper_grid.remove_widget(self.dripper_setting)
            self.dripper_setting = None
        if self.print_api:
            self.print_api.close()
        self.print_api = None
        self.ids.navigate_button.text_source = _('Cancel Print')
        self.ids.navigate_button.background_color = [2.0, 0.0, 0.0, 1.0]
        last_print = App.get_running_app().last_print
        if last_print.print_type is "file":
            self.print_file(last_print.source, self.return_to)
        elif last_print.print_type is "test_print":
            generator = self.api.get_test_print_api().get_test_print(*last_print.source)
            self.print_generator(generator, self.return_to)
        else:
            raise("Unsupported Print Type %s" % last_print.print_type)

    def play_complete_sound(self):
        sound_file = resource_find("complete.wav")
        if sound_file:
            sound = SoundLoader.load(sound_file)
            if sound:
                sound.play()
        else:
            Logger.warning("Sound was unfound")

    def play_failed_sound(self):
        sound_file = resource_find("fail.wav")
        if sound_file:
            sound = SoundLoader.load(sound_file)
            if sound:
                sound.play()
        else:
            Logger.warning("Sound was unfound")

    def on_pre_enter(self):
        for (title, value) in self.parent.setting_translation.get_settings().items():
            self.settings_popup.add_setting(ListElement(title=title, value=value))
        self.ids.navigate_button.text_source = _('Cancel Print')
        self.ids.navigate_button.background_color = [2.0, 0.0, 0.0, 1.0]

    def cancel_print(self):
        Logger.info("Print cancel requested")
        Clock.unschedule(self._update_status)
        self.parent.current = self.return_to

    def on_pre_leave(self):
        if self.dripper_setting:
            self.ids.dripper_grid.remove_widget(self.dripper_setting)
            self.dripper_setting = None
        Clock.unschedule(self._update_status)
        if self.print_api:
            self.print_api.close()
        self.ids.printer_animation.animation_stop()
        self.print_api = None
        self.settings_popup.remove_settings()
