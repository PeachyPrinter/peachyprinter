from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

from kivy.logger import Logger


Builder.load_file('ui/cure_test_ui.kv')

class CureTestUI(Screen):
    def __init__(self, **kwargs):
        super(CureTestUI, self).__init__(**kwargs)

    def update_image(self):
        Logger.info("Cure height: %s" % self.ids.cure_height.text)
        Logger.info("Cure width: %s" % self.ids.cure_width.text)
        Logger.info("Cure start speed: %s" % self.ids.cure_start_speed.text)
        Logger.info("Cure stop_ peed: %s" % self.ids.cure_stop_speed.text)
