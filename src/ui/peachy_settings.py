from kivy.uix.settings import SettingString
from kivy.properties import ListProperty
from kivy.compat import text_type

class SettingFloat(SettingString):
    value_range = ListProperty([None, None])
    foreground_color_valid = ListProperty([0.0, 0.0, 0.0, 1.0])
    foreground_color_invalid = ListProperty([1.0, 0.0, 0.0, 1.0])

    def __init__(self, **kwargs):
        super(SettingFloat, self).__init__(**kwargs)
        self.bind(textinput=self.on_entering_text)
        self.valid = True

    def is_valid(self, value):
        try:
            tmp_value = float(value)
            low_ok  = (self.value_range[0] is None or tmp_value >= self.value_range[0])
            high_ok = (self.value_range[1] is None or tmp_value <= self.value_range[1])
            if low_ok and high_ok:
                self.valid = True
                return True
        except ValueError:
            pass
        self.valid = False
        return False

    def _validate(self, instance):
        if self.is_valid(self.textinput.text):
            self.value = text_type(self.textinput.text)
            self._dismiss()

    def on_entering_text(self, instance, value):
        value.bind(cursor_pos=self.on_text_entered)
        self.last_value = value.text

    def on_text_entered(self, instance, value):
        try:
            float(instance.text)
            self.last_value = instance.text
        except ValueError:
            instance.text = self.last_value
        if self.is_valid(instance.text):
            instance.foreground_color = self.foreground_color_valid
        else:
            instance.foreground_color = self.foreground_color_invalid
