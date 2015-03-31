from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.graphics import *
from kivy.clock import Clock
import time

from ui.custom_widgets import BorderedLabel, LabelGridLayout
import os

from kivy.logger import Logger

class Dripper(BoxLayout):
    def __init__(self, **kwargs):
        super(Dripper, self).__init__(**kwargs)
        self.index = 0.0
        self.sections = 20
        self.section_height = 1
        self.lasttime = time.time()
        Clock.schedule_once(self.redraw)

    def update(self, data):
        self.drip_history = data['drip_history']

    def redraw(self, key):
        self.index += (time.time() - self.lasttime) * self.sections
        self.lasttime = time.time()
        if self.index > self.section_height * 2:
            self.index = 0
        self.draw()
        Clock.schedule_once(self.redraw, 1.0 / 60.0)

    def on_height(self, instance, value):
        self.section_height = self.height / self.sections

    def draw(self):
        self.canvas.clear()
        for i in range(0, self.sections + 3):
            if i % 2 == 0:
                self.canvas.add(Color(0.6, 0.65, 0.6, 1))
            else:
                self.canvas.add(Color(0.4, 0.45, 0.4, 1))
            p = (i * self.section_height) - self.index
            self.canvas.add(Rectangle(pos=(self.x, p), size=(self.width, self.section_height)))
            



class PrintStatus(LabelGridLayout):
    data_points = {
     'status': 'Status',
     'model_height': 'Model Height',
     'start_time': 'Start Time',
     'drips': 'Drips Counted',
     'height': 'Actual Height',
     'drips_per_second': 'Drips per second',
     'errors': 'Error List',
     'waiting_for_drips': 'Waiting for drip',
     'elapsed_time': 'Elapsed Time',
     'current_layer': 'Current Layer',
     'skipped_layers': 'Skipped Layers'
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

    def on_pre_enter(self):
        for (title, value) in self.parent.setting_translation.get_settings().items():
            title_label = BorderedLabel(text=title, bold=True, borders=[0, 1.0, 0, 0])
            value_label = BorderedLabel(text=value,  halign='right', borders=[0, 1.0, 1.0, 0])
            self.ids.print_settings.add_widget(title_label)
            self.ids.print_settings.add_widget(value_label)
        Logger.info("Path: %s>" % self.selected_file.filename)
        Logger.info("PrintUI Entered")
        filepath = self.selected_file.filename[0].encode('utf-8')

        self.print_api = self.api.get_print_api(status_call_back=self.callback)
        self.path = os.path.basename(filepath)
        self.print_api.print_gcode(filepath)

    def on_pre_leave(self):
        if self.print_api:
            self.print_api.close()
        self.print_api = None
        self.ids.print_settings.clear_widgets()
