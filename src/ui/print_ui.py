from kivy.uix.screenmanager import Screen
from kivy.graphics import *
from kivy.logger import Logger
from kivy.lang import Builder

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
            label = BorderedLabel(text=value, bold=True, borders=[0, 1.0, 0, 0])
            content = BorderedLabel(id=key, text="asd", halign='right', borders=[0, 1.0, 1.0, 0])
            self.add_widget(label)
            self.add_widget(content)

    def update(self, data):
        for child in self.children:
            if child.id is not "":
                if str(child.id) in data:
                    child.text = str(data[child.id])


class PrintingUI(Screen):
    def __init__(self, api, selected_file, **kwargs):
        super(PrintingUI, self).__init__(**kwargs)
        self.api = api
        self.print_api = None
        self.selected_file = selected_file

    def callback(self, data):
        self.ids.print_status.update(data)
        self.ids.dripper.update(data)

    def print_file(self, filename):
        try:
            filepath = filename[0].encode('utf-8')
            self.print_api = self.api.get_print_api(status_call_back=self.callback)
            self.path = os.path.basename(filepath)
            self.print_api.print_gcode(filepath)
        except Exception as ex:
            popup = ErrorPopup(title='Error', text=str(ex), size_hint=(0.6, 0.6))
            popup.open()
            self.parent.current = 'mainui'

    def print_generator(self, generator):
        try:
            self.print_api = self.api.get_print_api(status_call_back=self.callback)
            self.print_api.print_layers(generator)
        except Exception as ex:
            popup = ErrorPopup(title='Error', text=str(ex), size_hint=(0.6, 0.6))
            popup.open()
            self.parent.current = 'mainui'

    def on_pre_enter(self):
        for (title, value) in self.parent.setting_translation.get_settings().items():
            title_label = BorderedLabel(text=title, bold=True, borders=[0, 1.0, 0, 0])
            value_label = BorderedLabel(text=value,  halign='right', borders=[0, 1.0, 1.0, 0])
            self.ids.print_settings.add_widget(title_label)
            self.ids.print_settings.add_widget(value_label)

    def on_pre_leave(self):
        if self.print_api:
            self.print_api.close()
        self.print_api = None
        self.ids.print_settings.clear_widgets()
