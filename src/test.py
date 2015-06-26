from kivy.app import App
from ui.ddd_widgets import I18NObjImageButton
from infrastructure.langtools import _


def _(stn):
    return stn


class RendererApp(App):
    def _(self, s):
        return s

    def translation(self, text):
        return text

    def build(self):
        model = 'resources/objects/Simple5Sided180TwistVaseBETA.obj'
        text_source = _('Some Text')

        return I18NObjImageButton(model=model, text_source=text_source)

if __name__ == "__main__":
    RendererApp().run()
