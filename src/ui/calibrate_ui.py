from kivy.uix.screenmanager import Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ListProperty, StringProperty, NumericProperty, ObjectProperty, BooleanProperty
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.app import App
from infrastructure.langtools import _
from ui.custom_widgets import I18NTabbedPanelItem, ErrorPopup, I18NImageToggleButton
from ui.peachy_widgets import LaserWarningPopup

class SetupPanel(BoxLayout):
    calibration_api = ObjectProperty(None)

class CenterPanel(SetupPanel):
    def __init__(self,  **kwargs):
        super(CenterPanel, self).__init__(**kwargs)

    def on_enter(self):
        if self.calibration_api:
            self.calibration_api.show_point([0.5, 0.5, 0.0])


class PrintAreaPanel(SetupPanel):
    print_area_width = StringProperty("")
    print_area_depth = StringProperty("")
    print_area_height = StringProperty("")

    def __init__(self,  **kwargs):
        super(PrintAreaPanel, self).__init__(**kwargs)

    def on_enter(self):
        if self.calibration_api:
            self.calibration_api.show_scale()
            print_area_width, print_area_depth, print_area_height = self.calibration_api.get_print_area()
            self.ids.print_area_width.text = str(print_area_width)
            self.ids.print_area_depth.text = str(print_area_depth)
            self.ids.print_area_height.text = str(print_area_height)

    def on_leave(self,):
        self.calibration_api.set_print_area(float(self.ids.print_area_width.text), float(self.ids.print_area_depth.text), float(self.ids.print_area_height.text))


class AlignmentPanel(SetupPanel):

    def __init__(self, **kwargs):
        super(AlignmentPanel, self).__init__(**kwargs)

    def on_enter(self):
        if self.calibration_api:
            self.calibration_api.show_line()


class OrientationPanel(SetupPanel):
    orient_swap_axis = StringProperty("False")
    orient_xflip = StringProperty("False")
    orient_yflip = StringProperty("False")


    def __init__(self, **kwargs):
        super(OrientationPanel, self).__init__(**kwargs)

    def update_orientation(self, xflip, yflip, swap_axis):
        self.orient_swap_axis = "True" if swap_axis else "False"
        self.orient_xflip = "True" if xflip else "False"
        self.orient_yflip = "True" if yflip else "False"
        self.calibration_api.set_orientation(bool(xflip), bool(yflip), bool(swap_axis))

    def on_enter(self):
        if self.calibration_api:
            self.calibration_api.show_orientation()
            current = list(self.calibration_api.get_orientation())
            for child in self.ids.orientations.children:
                if child.configuration == current:
                    child.state = 'down'
                else:
                    child.state = 'normal'
            self.update_orientation(*current)


class CalibrationPanel(SetupPanel):
    calibration_type = StringProperty("top")
    calibration_height = NumericProperty(0)
    calibration_point = ListProperty([0, 0])
    calibration_point_color = ListProperty([1, 0, 0, 1])
    example_point = ListProperty([0, 0])
    example_dot = ListProperty([0, 0])
    printer_point = ListProperty([0.5, 0.5, calibration_height])
    printer_point_text = StringProperty('')
    printer_point_emphasis = BooleanProperty(False)
    center_point = ListProperty([0.0, 0.0])
    selected = ObjectProperty()
    valid = BooleanProperty(False)
    swap_axis = BooleanProperty()
    xflip = BooleanProperty()
    yflip = BooleanProperty()


    def __init__(self, **kwargs):
        super(CalibrationPanel, self).__init__(**kwargs)
        self.is_accurate = False
        self.bind(example_point=self.on_example_point)

    def set_points(self, peachy, example):
        self.printer_point = peachy
        self.example_point = example
        self.set_screen_point_from_printer()
        self.print_peachy_point()
        self.printer_point_emphasis = True
        if self._all_points_are_valid():
            self.valid = True

    def _all_points_are_valid(self):
        is_valid = True
        for child in self.ids.point_selections.children:
            is_valid = is_valid and child.valid
        return is_valid

    def reset_points(self):
        self.ids.point_selections.clear_widgets()
        self.valid = False

        for point in [[-1.0, 1.0], [1.0, 1.0], [1.0, -1.0], [-1.0, -1.0]]:
            c_point = CalibrationPoint(
                caller=self,
                active=False,
                actual=[point[0] * self.printer_width / 2.0, point[1] * self.printer_depth / 2.0],
                peachy=self.get_orientation_correction((point[0] / 2 + 1) / 2, (point[1] / 2 + 1) / 2),
                example=[(point[0] + 1) / 2, (point[1] + 1) / 2],
                valid=False,
                indicator_color=[1.0, 0.0, 0.0, 1.0],
                group="current",
            )
            self.ids.point_selections.add_widget(c_point)

    def on_resize(self, *args):
        Clock.schedule_once(self.fix_sizes, 0)

    def fix_sizes(self, *args):
        self.set_screen_point_from_printer()
        self.on_example_point()

    def on_example_point(self, *args):
        image_size = min(self.ids.example_grid.size)
        pos_x = self.ids.example_grid.x + (self.ids.example_grid.width - image_size) / 2
        pos_y = self.ids.example_grid.y + (self.ids.example_grid.height - image_size) / 2
        self.example_dot = [
            pos_x - 4 + (self.example_point[0] * image_size),
            pos_y - 4 + (self.example_point[1] * image_size),
            ]

    def get_orientation_correction(self, x, y):
        if self.xflip:
            x = 1.0 - x
        if self.yflip:
            y = 1.0 - y
        if self.swap_axis:
            xt, yt = x, y
            x, y = yt, xt
        return [x, y]

    def remove_orientation_correction(self, x, y):
        if self.swap_axis:
            xt, yt = x, y
            x, y = yt, xt
        if self.yflip:
            y = 1.0 - y
        if self.xflip:
            x = 1.0 - x
        return [x, y]

    def print_peachy_point(self):
        self.calibration_api.show_point([self.printer_point[0], self.printer_point[1], self.calibration_height])

    def super_accurate_mode(self):
        if self.ids.super_accurate.state == 'normal':
            self.is_accurate = False
            self.calibration_point_color = [1, 0, 0, 1]
            self.center_point = [0.0, 0.0]
            self.set_screen_point_from_printer()
        else:
            self.is_accurate = True
            self.calibration_point_color = [0.78, 0, 1, 1]
            self.center_point = self.remove_orientation_correction(*self.printer_point)
            self.calibration_point = self.ids.top_calibration_grid.center

    def set_screen_point_from_printer(self):
        grid_size = min(self.ids.top_calibration_grid.size)
        grid_extents = grid_size / 2.0
        grid_x = self.ids.top_calibration_grid.center[0] - grid_extents
        grid_y = self.ids.top_calibration_grid.center[1] - grid_extents

        xt, yt = self.remove_orientation_correction(self.printer_point[0], self.printer_point[1])

        Logger.info("Adjusted Printer Points %s,%s" % (xt, yt))

        rel_x = xt * grid_size
        rel_y = yt * grid_size

        self.calibration_point = [grid_x + rel_x, grid_y + rel_y]

    def set_printer_pos_from_screen(self, x, y):
        if self.is_accurate:
            dx = ((x * 2) - 1) * 0.1
            dy = ((y * 2) - 1) * 0.1
            peachyx = max(0, min(1.0, self.center_point[0] + dx))
            peachyy = max(0, min(1.0, self.center_point[1] + dy))
        else:
            peachyx = x
            peachyy = y

        self.printer_point = self.get_orientation_correction(peachyx, peachyy)
        self.print_peachy_point()

    def on_motion(self, etype, motionevent, mouse_pos):
        grid_size = min(self.ids.top_calibration_grid.size)
        grid_extents = grid_size / 2.0
        grid_x = self.ids.top_calibration_grid.center[0] - grid_extents
        grid_y = self.ids.top_calibration_grid.center[1] - grid_extents
        rel_x = mouse_pos.pos[0] - grid_x
        rel_y = mouse_pos.pos[1] - grid_y
        # Logger.info("X,Y -> %s,%s" % (rel_x, rel_y))
        if 0 <= rel_x and rel_x <= grid_size and 0 <= rel_y and rel_y <= grid_size:
            print_x = rel_x / grid_size
            print_y = rel_y / grid_size
            self.set_printer_pos_from_screen(print_x, print_y)
            self.calibration_point = mouse_pos.pos
        if motionevent == 'end':
            self._save_current_point()

    def _save_current_point(self):
        selected_point = [point for point in self.ids.point_selections.children if point.ids.toggle.state =='down']
        if selected_point:
            selected_point[0].save_point(self.printer_point)
            self.printer_point_emphasis = True
            if self._all_points_are_valid():
                self.valid = True

    def on_printer_point(self, instance, value):
        self.printer_point_emphasis = False
        self.printer_point_text = _('Printer Posisition || ') + 'X: %.1f, Y: %.1f' % ((value[0] * 200) - 100, (value[1] * 200) - 100)

    def load_points_from_exisiting_calibration(self):
        self.ids.point_selections.clear_widgets()
        self.valid = True

        if self.calibration_type == 'top':
            calibration_points = self.calibration_api.get_upper_points()
            height = self.calibration_api.get_height()
            if self.printer_height != height:
                self.reset_points()
                return
        else:
            calibration_points = self.calibration_api.get_lower_points()
            height = 0

        for (peachy, actual) in sorted(calibration_points.items(), key=lambda item: (item[1][0], item[1][1]), reverse=True):
            if abs(actual[0] * 2.0) != self.printer_width or abs(actual[1] * 2.0) != self.printer_depth:
                self.reset_points()
                return
            c_point = CalibrationPoint(
                caller=self,
                active=False,
                actual=actual,
                peachy=peachy,
                example=[(actual[0] / abs(actual[0]) + 1.0) / 2.0, (actual[1] / abs(actual[1]) + 1.0) / 2.0],
                valid=True,
                indicator_color=[0.0, 1.0, 0.0, 1.0],
                group="current",
            )
            self.ids.point_selections.add_widget(c_point)

    def disable_super_accurate_mode(self):
        self.ids.super_accurate.state = 'normal'
        self.super_accurate_mode()

    def save_all_points(self):
        points = dict([((child.peachy[0], child.peachy[1]), (child.actual[0], child.actual[1])) for child in self.ids.point_selections.children])
        if self.calibration_type == 'top':
            self.calibration_api.set_upper_points(points)
            self.calibration_api.set_height(self.printer_height)
        else:
            self.calibration_api.set_lower_points(points)

    def on_enter(self):
        Window.bind(on_motion=self.on_motion)
        Window.bind(on_resize=self.on_resize)
        self.printer_width, self.printer_depth, self.printer_height = self.calibration_api.get_print_area()

        if self.calibration_api:
            x, y, s = self.calibration_api.get_orientation()
            self.swap_axis = s
            self.xflip = x
            self.yflip = y
            Logger.info('X-%s, Y-%s, S-%s' % (str(self.swap_axis), str(self.xflip), str(self.yflip),))
            self.load_points_from_exisiting_calibration()
            self.print_peachy_point()

    def on_leave(self):
        self.save_all_points()
        Window.unbind(on_motion=self.on_motion)
        Window.unbind(on_resize=self.on_resize)


class CalibrationPoint(BoxLayout):
    active = BooleanProperty(False)
    actual = ListProperty([0.0, 0.0])
    peachy = ListProperty([0.0, 0.0])
    example = ListProperty([0.0, 0.0])
    valid = BooleanProperty()
    indicator_color = ListProperty([1.0, 0.0, 0.0, 1.0])
    toggle_text = StringProperty()
    group = StringProperty()
    caller = ObjectProperty()

    def __init__(self, **kwargs):
        super(CalibrationPoint, self).__init__(**kwargs)
        self.toggle_text = 'X:%.1f , Y:%.1f' % (self.actual[0], self.actual[1])

    def save_point(self, point):
        if not self._points_equal(point, self.peachy):
            self.valid = True
            self.indicator_color = [0.0, 1.0, 0.0, 1.0]
            self.peachy = point

    def _points_equal(self, p1, p2, error=0.001):
        return (abs(p1[0] - p2[0]) <= error) and (abs(p1[0] - p2[0]) <= error)

    def on_state(self, value):
        if value == 'down':
            self.caller.disable_super_accurate_mode()
            self.caller.set_points(self.peachy, self.example)

            self.active = True
        else:
            self.active = False


class TestPatternPanel(SetupPanel):
    speed = NumericProperty(100)
    current_height = NumericProperty(0.0)

    def __init__(self, **kwargs):
        super(TestPatternPanel, self).__init__(**kwargs)
        self.loaded = False

    def on_enter(self):
        if not self.loaded:
            items = self.calibration_api.get_test_patterns()
            for item in items:
                image_source = "resources/icons/laser_calibration-test_pattern_{0}-100x100.png".format(item.lower().replace(' ', '_'))
                self.ids.patterns.add_widget(I18NImageToggleButton(group='test_patterns',  text_source=item, source=image_source, on_release=self.show_pattern))
            self.calibration_api.set_test_pattern_speed(self.speed)
            self.ids.patterns.children[-1].state = "down"
            self.loaded = True
        for child in self.ids.patterns.children:
            if child.state == "down":
                self.show_pattern(child)
                break
        printer_width, printer_depth, printer_height = self.calibration_api.get_print_area()
        self.ids.current_height_slider.max = printer_height
        self.ids.current_height_slider.step = printer_height / 500

    def show_pattern(self, instance):
        Logger.info("Loading: %s" % instance.text_source)
        if self.loaded:
            self.calibration_api.show_test_pattern(instance.text_source)

    def on_speed(self, instance, value):
        if self.loaded:
            Logger.info("On Speed: %s" % value)
            self.calibration_api.set_test_pattern_speed(value)

    def on_current_height(self, instance, value):
        if self.loaded:
            Logger.info("On height: %s" % value)
            self.calibration_api.set_test_pattern_current_height(float(value))


Builder.load_file('ui/calibrate_ui.kv')


class CalibrateUI(Screen):
    calibration_api = ObjectProperty(None)

    def __init__(self, api, **kwargs):
        self.is_active = False
        super(CalibrateUI, self).__init__(**kwargs)
        self.api = api
        self.ids.center_panel.content = CenterPanel()
        self.ids.orientation_panel.content = OrientationPanel()
        self.ids.alignment_panel.content = AlignmentPanel()
        self.ids.print_area_panel.content = PrintAreaPanel()
        self.ids.calibration_panel_top.content = CalibrationPanel(calibration_type='top', calibration_height=666)
        self.ids.calibration_panel_bottom.content = CalibrationPanel(calibration_type='bottom', calibration_height=0)
        self.ids.test_pattern_panel.content = TestPatternPanel()

    def on_enter(self):
        popup = LaserWarningPopup()
        popup.bind(on_dismiss=self.is_safe)
        popup.open()

    def is_safe(self, instance):
        if instance.is_safe():
            self.turn_on()
        else:
            App.get_running_app().root.current = 'mainui'

    def turn_on(self):
        self.is_active = True
        try:
            self.calibration_api = self.api.get_calibration_api()
            self.calibration_api.show_point([0.5, 0.5, 0.0])
        except Exception as ex:
            import traceback
            traceback.print_exc()
            ep = ErrorPopup(title_source=_("Error"), text=_("No Peachy Printer Detected"), details="%s\n%s" % (type(ex), ex))
            ep.open()
            App.get_running_app().root.current = 'mainui'
        self._switch_to_default_panel()

    def on_calibration_api(self, instance, value):
        for an_id in self.ids:
            if hasattr(self.ids[an_id].content, 'calibration_api'):
                self.ids[an_id].content.calibration_api = value

    def on_pre_leave(self):
        self._switch_to_default_panel()
        self.is_active = False
        if self.calibration_api:
            self.calibration_api.close()
        self.calibration_api = False

    def _switch_to_default_panel(self):
        panel = self.ids.tab_panel.tab_list[-1]
        self.ids.tab_panel.switch_to(panel)
