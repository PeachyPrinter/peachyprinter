from kivy.uix.screenmanager import Screen
from kivy.properties import ListProperty
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.core.window import Window


Builder.load_file('ui/calibrate_ui.kv')


class CalibrateUI(Screen):
    calibration_point = ListProperty([0, 0])

    def __init__(self, **kwargs):
        super(CalibrateUI, self).__init__(**kwargs)

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


    def on_pre_enter(self):
        Window.bind(on_motion=self.on_motion)

    def on_pre_leave(self):
        Window.unbind(on_motion=self.on_motion)
