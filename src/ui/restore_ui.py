from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.app import App

from infrastructure.langtools import _
from ui.custom_widgets import ErrorPopup

Builder.load_file('ui/restore_ui.kv')


class RestoreUI(Screen):
    configuration_api = ObjectProperty()

    def __init__(self, api, **kwargs):
        super(RestoreUI, self).__init__(**kwargs)
        self.api = api

    def restore_defaults(self):
        self.configuration_api.reset_printer()

    def on_pre_enter(self):
        try:
            self.configuration_api = self.api.get_configuration_api()
        except Exception as ex:
            import traceback
            traceback.print_exc()
            ep = ErrorPopup(title_source=_("Error"), text=_("No Peachy Printer Detected"), details="%s\n%s" % (type(ex), ex))
            ep.open()
            App.get_running_app().root.current = 'mainui'
