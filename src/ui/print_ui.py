import datetime

from kivy.uix.screenmanager import Screen
from kivy.graphics import *
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty

from ui.custom_widgets import ErrorPopup
from ui.peachy_widgets import LaserWarningPopup
from infrastructure.langtools import _

import os

Builder.load_file('ui/print_ui.kv')


class ListElement(BoxLayout):
    title = StringProperty()
    value = StringProperty()


class PrinterAnimation(RelativeLayout):
    printer_actual_dimensions = ListProperty([80, 80, 80])
    printer_current_actual_height = NumericProperty(0.0)
    printer_pixel_height = NumericProperty(1)
    printer_pixel_width = NumericProperty(1)
    resin_pixel_height = NumericProperty(20)
    water_pixel_height = NumericProperty(20)
    resin_y = NumericProperty(0)

    scale = NumericProperty(1.0)

    resin_color = ListProperty([0.0, 1.0, 0.0, 0.3])
    water_color = ListProperty([0.0, 0.1, 1.0, 0.3])
    container_color = ListProperty([1.0, 1.0, 1.0, 1.0])
    padding = NumericProperty(40)


    def on_size(self, *largs):
        bounds_y = (self.height * 0.7) - self.resin_pixel_height
        bounds_x = self.width - (self.padding * 2)
        printer_x = self.printer_actual_dimensions[0]
        printer_y = self.printer_actual_dimensions[1]

        self.scale = min(bounds_y / printer_y, bounds_x / printer_x)
        self.printer_pixel_width = printer_x * self.scale
        self.printer_pixel_height = printer_y * self.scale

        self.water_pixel_height = (self.scale * self.printer_current_actual_height) - self.resin_pixel_height 


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
        super(PrintingUI, self).__init__(**kwargs)
        self.api = api
        self.print_api = None
        self.print_options = []

    def on_printer_dimensions(self, instance, value):
        self.ids.printer_animation.printer_actual_dimensions = value

    def on_model_height(self, instance, value):
        self.ids.printer_animation.printer_current_actual_height = value

    def time_delta_format(self, td):
        total_seconds = td.total_seconds()
        hours = int(total_seconds) / (60 * 60)
        remainder = int(total_seconds) % (60 * 60)
        minutes = remainder / 60
        return "{0}:{1:02d}".format(hours, minutes)

    def callback(self, data):
        if 'status' in data:
            self.status = data['status']
        if 'model_height' in data:
            self.model_height = data['model_height']
        if 'start_time' in data:
            self.start_time = data['start_time']
        if 'drips' in data:
            self.drips = data['drips']
        if 'height' in data:
            self.print_height = data['height']
        if 'drips_per_second' in data:
            self.drips_per_second = data['drips_per_second']
        if 'errors' in data:
            self.errors = data['errors']
        if 'waiting_for_drips' in data:
            self.waiting_for_drips = str(data['waiting_for_drips'])
        if 'elapsed_time' in data:
            self.elapsed_time = self.time_delta_format(data['elapsed_time'])
        if 'current_layer' in data:
            self.current_layer = data['current_layer']
        if 'skipped_layers' in data:
            self.skipped_layers = data['skipped_layers']

        if self.status == 'Complete':
            self.play_complete_sound()
            self.ids.navigate_button.text_source = _("Print Complete, Close")
        if self.status == 'Failed':
            self.play_failed_sound()
            self.ids.navigate_button.text_source = _("Print Failed, Close")

    def print_file(self, *args, **kwargs):
        self.print_options = [self._print_file, args, kwargs]
        popup = LaserWarningPopup(title=_('Laser Safety Notice'), size_hint=(0.6, 0.6))
        popup.bind(on_dismiss=self.is_safe)
        popup.open()

    def _print_file(self, filename, start_height=0.0, return_name='mainui', force_source_speed=False):
        self.return_to = return_name
        try:
            filepath = filename[0].encode('utf-8')
            self.print_api = self.api.get_print_api(start_height=start_height, status_call_back=self.callback)
            self.path = os.path.basename(filepath)
            self.print_api.print_gcode(filepath, force_source_speed=force_source_speed)
        except Exception as ex:
            popup = ErrorPopup(title='Error', text=str(ex), size_hint=(0.6, 0.6))
            popup.open()
            self.parent.current = self.return_to

    def is_safe(self, instance):
        if instance.is_safe():
            self.print_options[0](*self.print_options[1], **self.print_options[2])
        else:
            self.parent.current = self.return_to

    def print_generator(self, *args, **kwargs):
        self.print_options = [self._print_generator, args, kwargs]
        popup = LaserWarningPopup()
        popup.bind(on_dismiss=self.is_safe)
        popup.open()

    def _print_generator(self, generator, return_name='mainui', force_source_speed=False):
        self.return_to = return_name
        try:
            self.print_api = self.api.get_print_api(status_call_back=self.callback)
            self.print_api.print_layers(generator, force_source_speed=force_source_speed)
        except Exception as ex:
            popup = ErrorPopup(title='Error', text=str(ex), size_hint=(0.6, 0.6))
            popup.open()
            self.parent.current = self.return_to

    def restart(self):
        if self.print_api:
            self.print_api.close()
        self.print_api = None
        self.ids.navigate_button.text_source = _('Cancel Print')
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
            self.ids.print_settings.add_widget(ListElement(title=title, value=value))
        self.ids.navigate_button.text_source = _('Cancel Print')

    def on_pre_leave(self):
        if self.print_api:
            self.print_api.close()
        self.print_api = None
        self.ids.print_settings.clear_widgets()
