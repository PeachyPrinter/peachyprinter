from kivy.compat import text_type
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.properties import ListProperty, ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.settings import SettingItem, SettingSpacer
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget



class SettingBoolean(SettingItem):
    '''Implementation of a boolean setting on top of a :class:`SettingItem`. It
    is visualized with a :class:`~kivy.uix.switch.Switch` widget. By default,
    0 and 1 are used for values: you can change them by setting :attr:`values`.
    '''

    values = ListProperty(['0', '1'])
    '''Values used to represent the state of the setting. If you want to use
    "yes" and "no" in your ConfigParser instance::

        SettingBoolean(..., values=['no', 'yes'])

    .. warning::

        You need a minimum of two values, the index 0 will be used as False,
        and index 1 as True

    :attr:`values` is a :class:`~kivy.properties.ListProperty` and defaults to
    ['0', '1']
    '''


class SettingString(SettingItem):
    '''Implementation of a string setting on top of a :class:`SettingItem`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivy.uix.popup.Popup` with a
    :class:`~kivy.uix.textinput.Textinput` so the user can enter a custom
    value.
    '''

    popup = ObjectProperty(None, allownone=True)
    '''(internal) Used to store the current popup when it's shown.

    :attr:`popup` is an :class:`~kivy.properties.ObjectProperty` and defaults
    to None.
    '''

    textinput = ObjectProperty(None)
    '''(internal) Used to store the current textinput from the popup and
    to listen for changes.

    :attr:`textinput` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to None.
    '''

    ok_button_text = StringProperty("Ok")
    '''Used to store the desired text for the popup Ok button.

    :attr:`ok_button_text` is an :class:`~kivy.properties.StringProperty`
    and defaults to 'Ok'.
    '''

    cancel_button_text = StringProperty("Cancel")
    '''Used to store the desired text for the popup Cancel button.

    :attr:`cancel_button_text` is an :class:`~kivy.properties.StringProperty`
    and defaults to 'Cancel'.
    '''

    def on_panel(self, instance, value):
        if value is None:
            return
        self.bind(on_release=self._create_popup)

    def _dismiss(self, *largs):
        if self.textinput:
            self.textinput.focus = False
        if self.popup:
            self.popup.dismiss()
        self.popup = None

    def _write(self, instance):
        self._dismiss()
        value = self.textinput.text.strip()
        self.value = value

    def _valid_input(self, value):
        #Controls allowable characters eg. Just numbers
        return True

    def _valid_entry(self, value):
        #Controls allowable content. eg email address
        return True

    def _on_text(self, instance, value):
        if self._valid_input(value):
            self.last_value = value
        else:
            self.textinput.text = self.last_value
            return
        self._ok_button.disabled = not self._valid_entry(value)

    def _create_popup(self, instance):
        # create popup layout
        content = BoxLayout(orientation='vertical', spacing='5dp')
        popup_width = min(0.95 * Window.width, dp(500))
        self.popup = popup = Popup(
            title=self.title, content=content, size_hint=(None, None),
            size=(popup_width, '250dp'))

        # create the textinput used for numeric input
        self.textinput = textinput = TextInput(
            text=self.value, font_size='24sp', multiline=False,
            size_hint_y=None, height='42sp')
        self.last_value = self.value
        textinput.bind(text=self._on_text)
        self.textinput = textinput

        # construct the content, widget are used as a spacer
        content.add_widget(Widget())
        content.add_widget(textinput)
        content.add_widget(Widget())
        content.add_widget(SettingSpacer())

        # 2 buttons are created for accept or cancel the current value
        btnlayout = BoxLayout(size_hint_y=None, height='50dp', spacing='5dp')
        self._ok_button = Button(text=self.ok_button_text)
        self._ok_button.bind(on_release=self._write)
        btnlayout.add_widget(self._ok_button)
        btn = Button(text=self.cancel_button_text)
        btn.bind(on_release=self._dismiss)
        btnlayout.add_widget(btn)
        content.add_widget(btnlayout)

        # all done, open the popup !
        popup.open()


class SettingNumeric(SettingString):
    '''Implementation of a numeric setting on top of a :class:`SettingString`.
    It is visualized with a :class:`~kivy.uix.label.Label` widget that, when
    clicked, will open a :class:`~kivy.uix.popup.Popup` with a
    :class:`~kivy.uix.textinput.Textinput` so the user can enter a custom
    value.
    '''

    value_range = ListProperty([None, None])
    '''Values used to represent the minimum and maximum values inclusive. None
    can be specified for no limit. If you want to use positive values only in
    your ConfigParser instance::

        SettingNumeric(..., value_range=[0, None])

    .. warning::

        You need exactlt two values, the index 0 will be used as minimum,
        and index 1 as maxium

    :attr:`values` is a :class:`~kivy.properties.ListProperty` and defaults to
    [None, None]
    '''

    def _valid_input(self, value):
        is_float = '.' in str(self.value)
        try:
            if is_float:
                float(value)
            else:
                int(value)
        except ValueError:
            return False
        return True

    def _in_value_range(self, value):
        inlow = (self.value_range[0] is None) or (value >= self.value_range[0])
        inhigh = (self.value_range[1] is None) or (value <= self.value_range[1])
        return inlow and inhigh

    def _valid_entry(self, value):
        is_float = '.' in str(self.value)
        try:
            if is_float:
                return self._in_value_range(float(value))
            else:
                return self._in_value_range(int(value))
        except ValueError:
            return False

    def _write(self, instance):
        is_float = '.' in str(self.value)
        self._dismiss()
        try:
            if is_float:
                self.value = text_type(float(self.textinput.text))
            else:
                self.value = text_type(int(self.textinput.text))
        except ValueError:
            return
