from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import *
from kivy.clock import Clock
import time
from math import sin, pi

from kivy.lang import Builder


Builder.load_file('ui/peachy_widgets.kv')


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

