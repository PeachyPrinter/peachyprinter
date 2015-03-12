import json
import os
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.settings import SettingsWithSidebar
from kivy.resources import resource_find
from kivy.properties import ListProperty
from kivy.uix.popup import Popup
from kivy.logger import Logger
from kivy.config import Config
from kivy.clock import Clock
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics.shader import *
from kivy.graphics import *
import time

from setting_adapter import SettingsAdapter

class Bork(Widget):
    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find(os.path.join('resources', 'shaders', 'simpleshader.glsl'))
        self.mesh_points = ListProperty([])
        super(Bork, self).__init__(**kwargs)
        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)
        Clock.schedule_interval(self.update_glsl, 1 / 60.)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def update_glsl(self, *largs):
        asp = self.width / float(self.height)
        proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
        self.canvas['projection_mat'] = proj
        self.canvas['diffuse_light'] = (1.0, 1.0, 0.8)
        self.canvas['ambient_light'] = (0.1, 0.1, 0.1)
        self.rot.angle += 1

    def setup_scene(self):
        Color(1, 1, 1, 1)
        PushMatrix()
        Translate(0, 0, -3)
        self.rot = Rotate(1, 0, 1, 0)

        a = [-1.0, -1.0, 0.0,        -1.0, 1.0, 0.0,]
        b = [ 1.0, -1.0, 0.0,        -1.0, 1.0, 0.0,]
        c = [ 0.0,  1.0, 0.0,         1.0, 0.0, 0.0,]
        d = [ 0.0,  0.0, 1.0,         0.0, 0.0, 1.0,]
        data = [ 
                a, b, d,
                b, c, d,
                c, d, a,
                ]
        data = [item for sublist in data for item in sublist]
        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=data,
            indices=[0, 1, 2, 3, 4, 5, 6, 7, 8],
            fmt=[(b'v_pos', 3, b'float'), (b'v_normal', 3, b'float')],
            mode='triangles',
        )
        PopMatrix()


class ResizingLabel(Label):
    def __init__(self, **kwargs):
        super(ResizingLabel, self).__init__(**kwargs)
        # self.bind(size=self.update_font)

    def update_font(self, *arg, **kwargs):
        Logger.info('SIZE ' * 5)
        self.text_font = self.parent.y * 0.8
        self.text = str(time.time())


class Interface(FloatLayout):
    pass

class ConfigPopUp(Popup):
    pass

class SettingsApp(App):
    def __init__(self,):
        self.settings_adapter = SettingsAdapter()
        super(SettingsApp, self).__init__()
        # Config.set('input', 'mouse', 'disable_multitouch')
        # Config.set('input', 'mouse', 'enable')

    def build(self):
        self.settings_cls = SettingsWithSidebar
        self.use_kivy_settings = False
        self.interface = Interface()
        return self.interface

    def build_config(self, config):
        for (key, value) in self.settings_adapter.defaults().items():
            config.setdefaults(key, value)

    def build_settings(self, settings):
        settings.add_json_panel("Peachy Printer", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Main']))
        settings.add_json_panel("Audio Settings", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Audio']))
        settings.add_json_panel("Advanced Options", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Options']))
        # settings.add_json_panel("Dripper Setup", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Dripper']))
        # settings.add_json_panel("Calibration Data", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Calibration']))
        settings.add_json_panel("Email Setup", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Email']))
        settings.add_json_panel("Serial Setup", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Serial']))
        settings.add_json_panel("Circut Selection", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Circut']))
        settings.add_json_panel("Micro Controller Setup", self.config, data=json.dumps([setting for setting in self.settings_adapter.getSettings() if setting['section'] == 'Micro Controller']))

    def on_config_changed(self, config, section, key, value):
        print key, value

    def on_open_config(self, **kwargs):
        self.pop_up = ConfigPopUp()
        self.pop_up.open()

    def on_close_config(self, **kwargs):
        self.pop_up.dismiss()


if __name__ == '__main__':
    SettingsApp().run()