from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty, StringProperty
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.core.window import Window


Builder.load_file('ui/calibrate_ui.kv')

class Orientation(object):
    orient_rotated = StringProperty("False")
    orient_xflip = StringProperty("False")
    orient_yflip = StringProperty("False")

    def update_orientation(self, rotate, xflip, yflip):
        self.orient_rotated = "True" if rotate else "False"
        self.orient_xflip = "True" if xflip else "False"
        self.orient_yflip = "True" if yflip else "False"

class CalibrateUI(Screen, Orientation):
    calibration_point = ListProperty([0, 0])
    example_point = ListProperty([0, 0])
    example_dot = ListProperty([100, 100])

    def __init__(self, **kwargs):
        super(CalibrateUI, self).__init__(**kwargs)
        self.bind(example_point=self.on_example_point)


    def on_motion(self, etype, motionevent, mouse_pos):
        (x, y) = self.ids.top_calibration_grid.pos
        (grid_width, grid_height) = self.ids.top_calibration_grid.size
        (mousex, mousey) = mouse_pos.pos
        imagex = (mousex - x)
        imagey = (mousey - y)
        if imagex >= 0 and imagex <= grid_width and imagey >= 0 and imagey <= grid_height:
            Logger.info("Moved")
            peachyx = (imagex / grid_width * 2) - 1
            peachyy = (imagey / grid_height * 2) - 1
            Logger.info('%s, %s' % (peachyx, peachyy))
            self.calibration_point = mouse_pos.pos
            # CALL TO API HERE

    def on_upper_left(self):
        self.example_point = [0, 1]

    def on_upper_right(self):
        self.example_point = [1, 1]

    def on_lower_right(self):
        self.example_point = [1, 0]

    def on_lower_left(self):
        self.example_point = [0, 0]

    def on_pre_enter(self):
        Window.bind(on_motion=self.on_motion)

    def on_example_point(self, *args):
        image_size =  min(self.ids.example_grid.size)
        pos_x = self.ids.example_grid.x + (self.ids.example_grid.width - image_size) / 2
        pos_y = self.ids.example_grid.y + (self.ids.example_grid.height - image_size) / 2
        self.example_dot = [
            pos_x - 4 + (self.example_point[0] * image_size),
            pos_y - 4 + (self.example_point[1] * image_size),
            ]
        Logger.info("Called %s,%s" % (self.example_dot[0],self.example_dot[1]))

    def on_pre_leave(self):
        Window.unbind(on_motion=self.on_motion)
