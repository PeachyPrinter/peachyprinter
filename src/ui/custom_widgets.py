from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Line, Color, InstructionGroup
from kivy.properties import NumericProperty
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel
from infrastructure.langtools import _

import re


class ErrorPopup(Popup):
    def __init__(self, text=None, **kwargs):
        super(ErrorPopup, self).__init__(**kwargs)
        if text is None:
            text = _('Bad Stuff Happened')
        layout = BoxLayout(orientation='vertical')
        message = Label(text=text)
        close = Button(text=_("Close"), on_release=self.dismiss, size_hint=[1.0, 0.5])
        layout.add_widget(message)
        layout.add_widget(close)
        self.add_widget(layout)


class LabelGridLayout(GridLayout):
    text_padding_x = NumericProperty(0)
    child_height = NumericProperty(20)

    def add_widget(self, widget):
        super(LabelGridLayout, self).add_widget(widget)
        self._resize()

    def clear_widgets(self, children=None):
        super(LabelGridLayout, self).clear_widgets(children)
        self._resize()

    def remove_widget(self, widget):
        super(LabelGridLayout, self).remove_widget(widget)
        self._resize()

    def on_child_height(self, instance, value):
        self._resize()

    def on_size(self, instance, value):
        self._resize()

    def _resize(self):
        self.height = len(self.children) * self.child_height
        for child in self.children:
            child.text_size = [self.size[0] - self.text_padding_x, self.child_height]


class BorderedLabel(Label):
    def __init__(self, borders=[0, 0, 0, 0], **kwargs):
        super(BorderedLabel, self).__init__(**kwargs)
        self.bind(pos=self.update_border, size=self.update_border)
        self.borders = borders
        self.top_points = [0, 0, 0, 0]
        self.bottom_points = [0, 0, 0, 0]
        self.left_points = [0, 0, 0, 0]
        self.right_points = [0, 0, 0, 0]
        self._new = True

    def draw_border(self):
        with self.canvas.after:
            Color(1, 1, 1, 1)
            if self.borders[0]:
                self.top_border = Line(points=self.top_points, width=self.borders[0])
            if self.borders[1]:
                self.right_border = Line(points=self.right_points, width=self.borders[1])
            if self.borders[2]:
                self.bottom_border = Line(points=self.bottom_points, width=self.borders[2])
            if self.borders[3]:
                self.left_border = Line(points=self.left_points, width=self.borders[3])

    def update_border(self, *args):
        if self._new:
            self.draw_border()
            self._new = False
        else:
            if hasattr(self, 'top_border'):
                self.top_border.points =    [self.pos[0]               , self.pos[1] - self.size[1],        self.pos[0] + self.size[0], self.pos[1] - self.size[1]]
            if hasattr(self, 'right_border'):
                self.right_border.points =  [self.pos[0] + self.size[0], self.pos[1],                       self.pos[0] + self.size[0], self.pos[1] + self.size[1]]
            if hasattr(self, 'bottom_border'):
                self.bottom_border.points = [self.pos[0]               , self.pos[1],                       self.pos[0] + self.size[0], self.pos[1]               ]
            if hasattr(self, 'left_border'):
                self.left_border.points =   [self.pos[0]               , self.pos[1],                       self.pos[0]               , self.pos[1] + self.size[1]]


class FloatInput(TextInput):
    valid_characters = re.compile('[^0-9]')

    def __init__(self, **kwargs):
        super(FloatInput, self).__init__(**kwargs)
        self.multiline = False

    def insert_text(self, substring, from_undo=False):

        if '.' in self.text:
            string_value = re.sub(self.valid_characters, '', substring)
        else:
            string_value = '.'.join([re.sub(self.valid_characters, '', string_value) for string_value in substring.split('.', 1)])
        return super(FloatInput, self).insert_text(string_value, from_undo=from_undo)


class CommunicativeTabbedPanel(TabbedPanel):
    def __init__(self, **kwargs):
        super(CommunicativeTabbedPanel, self).__init__(**kwargs)
        self.last_tab = self.current_tab

    def on_current_tab(self, instance, value):
        if hasattr(self.last_tab, 'on_leave'):
            self.last_tab.on_leave()
        if hasattr(value, 'on_enter'):
            value.on_enter()
        self.last_tab = value

