from kivy.uix.screenmanager import Screen
from kivy.graphics import *
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.app import App
from kivy.core.audio import SoundLoader
from kivy.resources import resource_find

from ui.custom_widgets import BorderedLabel, LabelGridLayout, ErrorPopup
from ui.peachy_widgets import LaserWarningPopup
from infrastructure.langtools import _

import os

Builder.load_file('ui/print_ui.kv')


class PrintStatus(LabelGridLayout):
    data_points = {
     'status': _('Status'),
     'model_height': _('Model Height'),
     'start_time': _('Start Time'),
     'drips': _('Drips Counted'),
     'height': _('Actual Height'),
     'drips_per_second': _('Drips per second'),
     'errors': _('Error List'),
     'waiting_for_drips': _('Waiting for drip'),
     'elapsed_time': _('Elapsed Time'),
     'current_layer': _('Current Layer'),
     'skipped_layers': _('Skipped Layers')
    }

    def __init__(self, **kwargs):
        self.content = {}
        super(PrintStatus, self).__init__(**kwargs)
        for (key, value) in self.data_points.items():
            label = BorderedLabel(text_source=value, bold=True, borders=[0, 1.0, 0, 0])
            self.content[key] = BorderedLabel(id=key, text="asd", halign='right', borders=[0, 1.0, 1.0, 0])
            self.add_widget(label)
            self.add_widget(self.content[key])

    def update(self, data):
        if 'status' in data:
            self.content['status'].text = '{0}'.format(data['status'])
        if 'model_height' in data:
            self.content['model_height'].text = '{:.2f}'.format(data['model_height'])
        if 'start_time' in data:
            self.content['start_time'].text = '{0}'.format(data['start_time'].strftime("%H:%M"))
        if 'drips' in data:
            self.content['drips'].text = '{0:.0f}'.format(data['drips'])
        if 'height' in data:
            self.content['height'].text = '{:.2f}'.format(data['height'])
        if 'drips_per_second' in data:
            self.content['drips_per_second'].text = '{:.2f}'.format(data['drips_per_second'])
        if 'errors' in data:
            self.content['errors'].text = '{0}'.format(','.join([str(error['message']) for error in data['errors']]))
        if 'waiting_for_drips' in data:
            self.content['waiting_for_drips'].text = '{0}'.format(data['waiting_for_drips'])
        if 'elapsed_time' in data:
            self.content['elapsed_time'].text = '~{0}'.format(self.time_delta_format(data['elapsed_time']))
        if 'current_layer' in data:
            self.content['current_layer'].text = '{0}'.format(data['current_layer'])
        if 'skipped_layers' in data:
            self.content['skipped_layers'].text = '{0}'.format(data['skipped_layers'])

    def time_delta_format(self, td):
        total_seconds = td.total_seconds()
        hours = int(total_seconds) / (60 * 60)
        remainder = int(total_seconds) % (60 * 60)
        minutes = remainder / 60
        return "{0}:{1:02d}".format(hours, minutes)


class PrintingUI(Screen):
    def __init__(self, api, **kwargs):
        self.return_to = 'mainui'
        super(PrintingUI, self).__init__(**kwargs)
        self.api = api
        self.print_api = None
        self.print_options = []

    def callback(self, data):
        self.ids.print_status.update(data)
        self.ids.dripper.update(data)
        if data['status'] == 'Complete':
            self.play_complete_sound()
            self.ids.navigate_button.text_source = _("Print Complete, Close")
        if data['status'] == 'Failed':
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
            title_label = BorderedLabel(text_source=title, bold=True, borders=[0, 1.0, 0, 0])
            value_label = BorderedLabel(text_source=value,  halign='right', borders=[0, 1.0, 1.0, 0])
            self.ids.print_settings.add_widget(title_label)
            self.ids.print_settings.add_widget(value_label)
        self.ids.navigate_button.text_source = _('Cancel Print')

    def on_pre_leave(self):
        if self.print_api:
            self.print_api.close()
        self.print_api = None
        self.ids.print_settings.clear_widgets()
