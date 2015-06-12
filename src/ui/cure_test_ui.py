from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import BoundedNumericProperty, BooleanProperty, StringProperty, NumericProperty, OptionProperty
from kivy.logger import Logger
from kivy.metrics import sp
from ui.custom_widgets import HorizontalLabelSlider

Builder.load_file('ui/cure_test_ui.kv')


class BaseSpeed(HorizontalLabelSlider):
    pass


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
        self.ids.total_height_id.value = max(self.base + 10, self.test_height)

    def show_base_speed(self, value):
        if value is True:
            self.use_base_speed = True
            self.ids.cure_test_panel_id.add_widget(self.base_speed, index=2)
        else:
            self.use_base_speed = False
            self.ids.cure_test_panel_id.remove_widget(self.base_speed)

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
            Logger.info("Saving draw_speed value of %.2f" % float(value))
            self.configuration_api.set_cure_rate_draw_speed(float(value))
            self.configuration_api.save()

    def on_move_speed(self, instance, value):
        if self.loaded:
            Logger.info("Saving move_speed value of %.2f" % float(value))
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

    def on_touch_down(self, touch):
        super(CureTestUI, self).on_touch_down(touch)
        self.touched(touch)

    def on_touch_move(self, touch):
        super(CureTestUI, self).on_touch_move(touch)
        self.touched(touch)

    def touched(self, touch):
        coords = self.ids.test_height_image_id.to_widget(*touch.pos)
        if self.ids.test_height_image_id.collide_point(*coords):
            self.ids.best_height_image_id.y = coords[1]
            self.ids.best_height_image_id.alpha = 1.0
            self.ids.selected_height_id.color = [1., 1., 1., 1.]
            self.ids.selected_speed_id.color = [1., 1., 1., 1.]
            return True


    def print_now(self):
        if self.use_base_speed:
            base_speed = self.base_speed.value
        else:
            base_speed = None
        generator = self.configuration_api.get_cure_test(self.base, self.test_height, self.start_speed, self.stop_speed, base_speed)
        self.manager.current = 'printingui'
        self.manager.printing_ui.print_generator(generator, self.name, force_source_speed=True)

    def on_pre_enter(self):
        self.configuration_api = self.api.get_configuration_api()
        self.ids.base_height_id.value = self.configuration_api.get_cure_rate_base_height()
        self.ids.total_height_id.value = self.configuration_api.get_cure_rate_total_height()
        self.ids.minimum_speed_id.value = self.configuration_api.get_cure_rate_start_speed()
        self.ids.maximum_speed_id.value = self.configuration_api.get_cure_rate_finish_speed()
        self.ids.use_draw_speed_id.active = self.configuration_api.get_cure_rate_use_draw_speed()
        self.ids.draw_speed_id.text = '%.2f' % self.configuration_api.get_cure_rate_draw_speed()
        self.ids.move_speed_id.text = '%.2f' % self.configuration_api.get_cure_rate_move_speed()
        self.ids.override_laser_power_id.active = self.configuration_api.get_cure_rate_override_laser_power()
        self.ids.override_laser_power_amount_id.text = '%.2f' % self.configuration_api.get_cure_rate_override_laser_power_amount()

    def on_enter(self):
        self.loaded = True
        Logger.info("Loaded")

    def on_pre_leave(self):
        self.configuration_api = False
        self.loaded = False
