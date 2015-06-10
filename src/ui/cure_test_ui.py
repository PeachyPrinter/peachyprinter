from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BoundedNumericProperty, BooleanProperty, StringProperty, NumericProperty, OptionProperty
from kivy.logger import Logger
from kivy.metrics import sp


Builder.load_file('ui/cure_test_ui.kv')


class HorizontalLabelSlider(BoxLayout):
    title = StringProperty()
    unit = StringProperty()
    value = NumericProperty(0.)
    min_value = NumericProperty(0.)
    max_value = NumericProperty(1.)
    step = BoundedNumericProperty(0, min=0)

class VerticalLabelSlider(BoxLayout):
    title = StringProperty()
    unit = StringProperty()
    value = NumericProperty(0.)
    min_value = NumericProperty(0.)
    max_value = NumericProperty(1.)
    step = BoundedNumericProperty(0, min=0)


class BaseSpeed(BoxLayout):
    base_speed = BoundedNumericProperty(150.0, min=0.0001, max=None)

class CureTestUI(Screen):
    max_height = NumericProperty(100)
    
    base = BoundedNumericProperty(10.0, min=0.00, max=None)
    test_height = BoundedNumericProperty(10.0, min=0.0001, max=None)
    start_speed = BoundedNumericProperty(100.0, min=0.0001, max=None)
    stop_speed = BoundedNumericProperty(200.0, min=0.0001, max=None)
    use_base_speed = BooleanProperty(False)
    use_draw_speed = BooleanProperty(False)
    draw_speed = BoundedNumericProperty(100.0, min=0.0001, max=None)
    move_speed = BoundedNumericProperty(100.0, min=0.0001, max=None)
    override_laser_power = BooleanProperty(False)
    override_laser_power_amount = BoundedNumericProperty(0.01, min=0, max=1)

    def __init__(self, api, **kwargs):
        self.api = api
        self.configuration_api = None
        self.loaded = False
        super(CureTestUI, self).__init__(**kwargs)
        self.base_speed = BaseSpeed()

    def show_base_speed(self, value):
        if value is True:
            self.use_base_speed = True
            self.ids.cure_test_panel.height += self.base_speed.height
            self.ids.cure_test_panel.add_widget(self.base_speed, index=5)
        else:
            self.use_base_speed = False 
            self.ids.cure_test_panel.height -= self.base_speed.height
            self.ids.cure_test_panel.remove_widget(self.base_speed)

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

    def on_draw_speed(self, instance, value):
        if self.loaded:
            Logger.info("Saving move_speed value of%.2f" % float(value))
            self.configuration_api.set_cure_rate_move_speed(float(value))
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
        if self.use_base_speed:
            base_speed = self.base_speed.base_speed
        else:
            base_speed = None
        generator = self.configuration_api.get_cure_test(self.base, self.test_height, self.start_speed, self.stop_speed, base_speed)
        self.manager.current = 'printingui'
        self.manager.printing_ui.print_generator(generator, self.name, force_source_speed=True)

    def on_pre_enter(self):
        self.configuration_api = self.api.get_configuration_api()
        # self.ids.base_id.text = '%.2f' % self.configuration_api.get_cure_rate_base_height()
        # self.ids.height_id.text = '%.2f' % self.configuration_api.get_cure_rate_total_height()
        # self.ids.start_speed_id.text = '%.2f' % self.configuration_api.get_cure_rate_start_speed()
        # self.ids.stop_speed_id.text = '%.2f' % self.configuration_api.get_cure_rate_finish_speed()
        # self.ids.use_draw_speed_id.active = self.configuration_api.get_cure_rate_use_draw_speed()
        # self.ids.draw_speed_id.text = '%.2f' % self.configuration_api.get_cure_rate_draw_speed()
        # self.ids.move_speed_id.text = '%.2f' % self.configuration_api.get_cure_rate_move_speed()
        # self.ids.override_laser_power_id.active = self.configuration_api.get_cure_rate_override_laser_power()
        # self.ids.override_laser_power_amount_id.text = '%.2f' % self.configuration_api.get_cure_rate_override_laser_power_amount()

    def on_enter(self):
        self.loaded = True
        Logger.info("Loaded")

    def on_pre_leave(self):
        self.configuration_api = False
        self.loaded = False
