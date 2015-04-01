from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty, StringProperty, NumericProperty
from kivy.uix.screenmanager import Screen
from kivy.graphics import *
from kivy.clock import Clock
import time
from math import sin, pi

from ui.custom_widgets import BorderedLabel, LabelGridLayout, ErrorPopup
from infrastructure.langtools import _

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
        self.drip_history = []
        self.count = 0

    def update(self, data):
        self.drip_history = data['drip_history']
        self.count = data['drips']

    def redraw(self, key):
        self.index += (time.time() - self.lasttime) * self.sections
        self.lasttime = time.time()
        if self.index > self.section_height * 2:
            self.index = 0
        self.draw()
        Clock.schedule_once(self.redraw, 1.0 / 30.0)

    def on_height(self, instance, value):
        self.section_height = self.height / self.sections

    def draw(self):
        self.canvas.clear()
        top = time.time()
        bottom = top - self.sections
        for (index, drip) in zip(range(len(self.drip_history),0,-1), self.drip_history):
            if drip > bottom:
                self.canvas.add(Color(0.0, 0.0, 1.0, 1.0))
                y = ((drip - bottom) / self.sections) * self.height
                s = sin((self.count - index) / (2 * pi))
                self.canvas.add(Ellipse(pos=(self.x + abs(self.width / 2.0 * s), y), size=(self.width / 5.0, 5)))


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

    def on_pre_enter(self):
        for (title, value) in self.parent.setting_translation.get_settings().items():
            title_label = BorderedLabel(text=title, bold=True, borders=[0, 1.0, 0, 0])
            value_label = BorderedLabel(text=value,  halign='right', borders=[0, 1.0, 1.0, 0])
            self.ids.print_settings.add_widget(title_label)
            self.ids.print_settings.add_widget(value_label)
        Logger.info("Path: %s>" % self.selected_file.filename)
        Logger.info("PrintUI Entered")
        filepath = self.selected_file.filename[0].encode('utf-8')
        try:
            self.print_api = self.api.get_print_api(status_call_back=self.callback)
            self.path = os.path.basename(filepath)
            self.print_api.print_gcode(filepath)
        except Exception as ex:
            popup = ErrorPopup(title='Error', text=str(ex), size_hint=(0.6, 0.6))
            popup.open()
            self.parent.current = 'mainui'

    def on_pre_leave(self):
        if self.print_api:
            self.print_api.close()
        self.print_api = None
        self.ids.print_settings.clear_widgets()
