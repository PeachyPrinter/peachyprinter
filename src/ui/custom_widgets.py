from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.graphics import Line, Color, InstructionGroup
from kivy.properties import NumericProperty, StringProperty
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.accordion import AccordionItem
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder


from infrastructure.langtools import _

import re

Builder.load_file('ui/custom_widgets.kv')


class I18NLabel(Label):
    text_source = StringProperty('')


class I18NButton(Button):
    text_source = StringProperty('')


class I18NToggleButton(Button):
    text_source = StringProperty('')


class I18NPopup(Popup):
    title_source = StringProperty('')


class I18NTabbedPanelItem(TabbedPanelItem):
    text_source = StringProperty('')


class I18NAccordionItem(AccordionItem):
    title_source = StringProperty('')


class I18NImageButton(Button):
    text_source = StringProperty()
    source = StringProperty()


class ErrorPopup(I18NPopup):
    text = StringProperty()
    details = StringProperty()

    def __init__(self, text=None, details=None, title_source=None, **kwargs):
        if text is None:
            self.text = _('Bad Stuff Happened')
        else:
            self.text = text
        if title_source is None:
            self.title_source = _("No Title")
        else:
            self.title_source = title_source
        if details is None:
            self.details = ""
        else:
            self.details = details
        super(ErrorPopup, self).__init__(**kwargs)


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
        self.height = str(len(self.children) * self.child_height) + "dp"
        for child in self.children:
             child.text_size = [self.size[0] - self.text_padding_x, child.height]


class BorderedLabel(I18NLabel):
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
