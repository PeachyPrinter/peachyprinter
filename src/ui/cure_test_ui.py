from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.properties import BoundedNumericProperty, BooleanProperty
from kivy.logger import Logger


Builder.load_file('ui/cure_test_ui.kv')


class CureTestUI(Screen):
    base = BoundedNumericProperty(10.0, min=0.0001, max=None)
    test_height = BoundedNumericProperty(10.0, min=0.0001, max=None)
    start_speed = BoundedNumericProperty(100.0, min=0.0001, max=None)
    stop_speed = BoundedNumericProperty(200.0, min=0.0001, max=None)
    use_draw_speed = BooleanProperty(False)
    draw_speed = BoundedNumericProperty(100.0, min=0.0001, max=None)
    override_laser_power = BooleanProperty(False)
    override_laser_power_amount = BoundedNumericProperty(0.01, min=0, max=1)

    def __init__(self, api, **kwargs):
        self.api = api
        self.configuration_api = None
        self.loaded = False
        super(CureTestUI, self).__init__(**kwargs)

    def on_base(self, instance, value):
        if self.loaded:
            Logger.info("Saving base value of %.2f" % float(value))
            self.configuration_api.set_cure_rate_base_height(float(value))
            self.configuration_api.save()

    def on_test_height(self, instance, value):
        if self.loaded:
            Logger.info("Saving height value of %.2f" % float(value))
            self.configuration_api.set_cure_rate_total_height(float(value))
            self.configuration_api.save()

    def on_start_speed(self, instance, value):
        if self.loaded:
            Logger.info("Saving start_speed value of %.2f" % float(value))
            self.configuration_api.set_cure_rate_start_speed(float(value))
            self.configuration_api.save()

    def on_stop_speed(self, instance, value):
        if self.loaded:
            Logger.info("Saving stop_speed value of %.2f" % float(value))
            self.configuration_api.set_cure_rate_finish_speed(float(value))
            self.configuration_api.save()

    def on_use_draw_speed(self, instance, value):
        if self.loaded:
            Logger.info("Saving use_draw_speed value of %s" % value)
            self.configuration_api.set_cure_rate_use_draw_speed(value)
            self.configuration_api.save()

    def on_draw_speed(self, instance, value):
        if self.loaded:
            Logger.info("Saving draw_speed value of%.2f" % float(value))
            self.configuration_api.set_cure_rate_draw_speed(float(value))
            self.configuration_api.save()

    def on_override_laser_power(self, instance, value):
        if self.loaded:
            Logger.info("Saving override_laser_power value of %s" % value)
            self.configuration_api.set_cure_rate_override_laser_power(value)
            self.configuration_api.save()

    def on_override_laser_power_amount(self, instance, value):
        if self.loaded:
            Logger.info("Saving override_laser_power_amount value of %.2f" % float(value))
            self.configuration_api.set_cure_rate_override_laser_power_amount(float(value))
            self.configuration_api.save()

    def print_now(self):
        generator = self.configuration_api.get_cure_test(self.base, self.test_height, self.start_speed, self.stop_speed)
        self.manager.current = 'printingui'
        self.manager.printing_ui.print_generator(generator, self.name)

    def on_pre_enter(self):
        self.configuration_api = self.api.get_configuration_api()
        self.ids.base_id.text = '%.2f' % self.configuration_api.get_cure_rate_base_height()
        self.ids.height_id.text = '%.2f' % self.configuration_api.get_cure_rate_total_height()
        self.ids.start_speed_id.text = '%.2f' % self.configuration_api.get_cure_rate_start_speed()
        self.ids.stop_speed_id.text = '%.2f' % self.configuration_api.get_cure_rate_finish_speed()
        self.ids.use_draw_speed_id.active = self.configuration_api.get_cure_rate_use_draw_speed()
        self.ids.draw_speed_id.text = '%.2f' % self.configuration_api.get_cure_rate_draw_speed()
        self.ids.override_laser_power_id.active = self.configuration_api.get_cure_rate_override_laser_power()
        self.ids.override_laser_power_amount_id.text = '%.2f' % self.configuration_api.get_cure_rate_override_laser_power_amount()

    def on_enter(self):
        self.loaded = True
        Logger.info("Loaded")

    def on_pre_leave(self):
        self.configuration_api = False
        self.loaded = False
