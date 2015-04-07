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


Builder.load_file('ui/library_ui.kv')


class PrintPop(Popup):
    def __init__(self, name, **kwargs):
        self.title = name
        super(PrintPop, self).__init__(**kwargs)
    def image(self):
        return os.path.join('resources', 'library_prints', 'missing.png')


class LibraryUI(Screen):
    def __init__(self, api, **kwargs):
        super(LibraryUI, self).__init__(**kwargs)
        self.api = api
        library_names = self.api.get_test_print_api().test_print_names()
        for name in library_names:
            image_path = os.path.join('resources', 'library_prints', name)
            if not os.path.isfile(image_path):
                image_path = os.path.join('resources', 'library_prints', 'missing.png')
            pict_button = Button(on_release=self.print_a,  text=name)
            self.ids.library_grid.add_widget(pict_button)


    def print_a(self, instance):
        PrintPop(instance.text).open()

