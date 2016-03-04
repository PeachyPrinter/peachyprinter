from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from kivy.clock import Clock
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.popup import Popup
from kivy.uix.image import Image
import time
from math import sin, pi

from kivy.lang import Builder
from kivy.loader import Loader
from kivy.logger import Logger
from ui.custom_widgets import I18NPopup, I18NLabel


Builder.load_file('ui/peachy_widgets.kv')


class TouchyLabel(I18NLabel):

    is_on = BooleanProperty(False)

    def on_touch_down(self, touch):
        if touch.is_triple_tap:
            self.is_on = not self.is_on


class I18NHelpPopup(I18NPopup):
    text_source = StringProperty()


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

    def update_parts(self, drips, history):
        self.drip_history = history
        self.count = drips

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
        self.canvas.add(Color(0.99, 0.99, 0.6, 1.0))
        self.canvas.add(Rectangle(pos=self.pos, size=self.size))
        for (index, drip) in zip(range(len(self.drip_history), 0, -1), self.drip_history):
            if drip > bottom:
                self.canvas.add(Color(0.35, 0.4, 1.0, 1.0))
                y = ((drip - bottom) / self.sections) * self.height
                s = sin((self.count - index) / (2 * pi))
                self.canvas.add(Ellipse(pos=(self.x + abs(self.width / 2.0 * s), y), size=(self.width / 5.0, 5)))


class LaserWarningPopup(I18NPopup):
    text_source = StringProperty()
    accepted = StringProperty(None)

    def __init__(self, **kwargs):
        super(LaserWarningPopup, self).__init__(**kwargs)
        self.countdown_image = Image(source="resources/images/laser_safety_countdown-256x256.zip", anim_delay=-1, anim_loop=1)

    def phase2(self):
        self.buttons.remove_widget(self.laser_on_button)
        self.container.remove_widget(self.markup)
        self.container.add_widget(self.countdown_image, index=2)
        Clock.schedule_once(self.phase3)

    def phase3(self, *args):
        self.countdown_image.anim_delay = (1.0 / 15.0)
        Clock.schedule_once(self.is_accepted, 3.7)

    def is_accepted(self, *args):
        if self.accepted != "False":
            self.accepted = "True"
        self.dismiss()

    def is_safe(self):
        if self.accepted is "True":
            return True
        return False


class LaserStatusBar(BoxLayout):
    def __init__(self, **kwargs):
        super(LaserStatusBar, self).__init__(**kwargs)
        self._last_message = None

    def update_message(self, printer_status_message):
        self._last_message = printer_status_message
        Clock.schedule_once(self._update)

    def _update(self, *args):
        if self._last_message:
            self.key_state = self._last_message.keyInserted
            self.switch_state = self._last_message.overrideSwitch
            self.card_state = self._last_message.cardInserted
            self.laser_state = self._last_message.laserOn

    def on_touch_up(self, touch):
        if (touch.x > self.x and
            touch.x < (self.x+self.width) and
            touch.y > self.y and
            touch.y < (self.y + self.height)):
                self.popup()
        super(LaserStatusBar, self).on_touch_down(touch)

    def popup(self):
        popup = LaserStatusDescriptionsPopup()
        popup.open()


class LaserStatusDescriptionsPopup(I18NPopup):
    pass