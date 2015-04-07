from kivy.uix.screenmanager import Screen
from kivy.lang import Builder


Builder.load_file('ui/cure_test_ui.kv')

class CureTestUI(Screen):
    def __init__(self, **kwargs):
        super(CureTestUI, self).__init__(**kwargs)