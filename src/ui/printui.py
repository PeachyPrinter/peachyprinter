from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from ui.custom_widgets import BorderedLabel
import os

from kivy.logger import Logger

# class PrintStatus(BoxLayout):
#     path = StringProperty("")

class PrintingUI(Screen):
    path = StringProperty("")
    def __init__(self, api, selected_file, **kwargs):
        super(PrintingUI, self).__init__(**kwargs)
        self.api = api
        self.selected_file = selected_file

    def on_pre_enter(self):
        for (title, value) in self.parent.setting_translation.get_settings().items():
            title_label = BorderedLabel(text=title, bold=True, borders=[0, 1.0, 0, 0])
            value_label = BorderedLabel(text=value,  halign='right', borders=[0, 1.0, 1.0, 0])
            self.ids.print_settings.add_widget(title_label)
            self.ids.print_settings.add_widget(value_label)
        Logger.info("Path: %s>" % self.selected_file.filename)
        Logger.info("PrintUI Entered")
        self.path = self.selected_file.filename[0].encode('utf-8')

    def on_pre_leave(self):
        self.ids.print_settings.clear_widgets()
