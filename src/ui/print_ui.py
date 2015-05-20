from kivy.uix.screenmanager import Screen
from kivy.graphics import *
from kivy.logger import Logger
from kivy.lang import Builder
from kivy.app import App
from ui.custom_widgets import BorderedLabel, LabelGridLayout, ErrorPopup
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
        super(PrintStatus, self).__init__(**kwargs)
        for (key, value) in self.data_points.items():
            label = BorderedLabel(text_source=value, bold=True, borders=[0, 1.0, 0, 0])
            content = BorderedLabel(id=key, text="asd", halign='right', borders=[0, 1.0, 1.0, 0])
            self.add_widget(label)
            self.add_widget(content)

    def update(self, data):
        for child in self.children:
            if child.id is not "":
                if str(child.id) in data:
                    child.text = str(data[child.id])


class PrintingUI(Screen):
    def __init__(self, api, **kwargs):
        self.return_to = 'mainui'
        super(PrintingUI, self).__init__(**kwargs)
        self.api = api
        self.print_api = None

    def callback(self, data):
        self.ids.print_status.update(data)
        self.ids.dripper.update(data)
        if data['status'] == 'Complete':
            self.ids.navigate_button.text = _("Print Complete, Close")

    def print_file(self, filename, return_name='mainui'):
        self.return_to = return_name
        try:
            filepath = filename[0].encode('utf-8')
            self.print_api = self.api.get_print_api(status_call_back=self.callback)
            self.path = os.path.basename(filepath)
            self.print_api.print_gcode(filepath)
        except Exception as ex:
            popup = ErrorPopup(title='Error', text=str(ex), size_hint=(0.6, 0.6))
            popup.open()
            self.parent.current = self.return_to

    def print_generator(self, generator, return_name='mainui'):
        self.return_to = return_name
        try:
            self.print_api = self.api.get_print_api(status_call_back=self.callback)
            self.print_api.print_layers(generator)
        except Exception as ex:
            popup = ErrorPopup(title='Error', text=str(ex), size_hint=(0.6, 0.6))
            popup.open()
            self.parent.current = self.return_to

    def restart(self):
        if self.print_api:
            self.print_api.close()
        self.print_api = None
        self.ids.navigate_button.text = _('Cancel Print')
        last_print = App.get_running_app().last_print
        if last_print.print_type is "file":
            self.print_file(last_print.source, self.return_to)
        elif last_print.print_type is "test_print":
            generator = self.api.get_test_print_api().get_test_print(*last_print.source)
            self.print_generator(generator, self.return_to)
        else:
            raise("Unsupported Print Type %s" % last_print.print_type)

    def on_pre_enter(self):
        for (title, value) in self.parent.setting_translation.get_settings().items():
            title_label = BorderedLabel(text_source=title, bold=True, borders=[0, 1.0, 0, 0])
            value_label = BorderedLabel(text_source=value,  halign='right', borders=[0, 1.0, 1.0, 0])
            self.ids.print_settings.add_widget(title_label)
            self.ids.print_settings.add_widget(value_label)

    def on_pre_leave(self):
        if self.print_api:
            self.print_api.close()
        self.print_api = None
        self.ids.print_settings.clear_widgets()
