import os
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.app import App

from ui.custom_widgets import I18NPopup


Builder.load_file('ui/library_ui.kv')


class PrintPop(I18NPopup):
    name = StringProperty()

    def __init__(self, api, screen_manager, **kwargs):
        self.screen_manager = screen_manager
        super(PrintPop, self).__init__(**kwargs)
        self.test_print_api = api

    def image(self):
        return os.path.join('resources', 'library_prints', 'missing.png')

    def print_from_library(self):
        name = self.title
        height = float(self.ids.height.text)
        width = float(self.ids.width.text)
        layer_height = float(self.ids.layer_height.text)
        speed = float(self.ids.speed.text)
        generator = self.test_print_api.get_test_print(name, height, width, layer_height, speed)
        self.screen_manager.current = 'printingui'
        self.screen_manager.printing_ui.print_generator(generator)


class LibraryUI(Screen):
    def __init__(self, api, **kwargs):
        super(LibraryUI, self).__init__(**kwargs)
        self.api = api
        self.test_print_api = self.api.get_test_print_api()
        library_names = self.test_print_api.test_print_names()
        for name in library_names:
            image_path = os.path.join('resources', 'library_prints', name)
            if not os.path.isfile(image_path):
                image_path = os.path.join('resources', 'library_prints', 'missing.png')
            pict_button = Button(on_release=self.print_a,  text=name)
            self.ids.library_grid.add_widget(pict_button)

    def print_a(self, instance):
        PrintPop(name=instance.text, api=self.test_print_api, screen_manager=self.parent).open()

