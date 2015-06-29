from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.resources import resource_find

from infrastructure.object_loader import ObjFile
from infrastructure.langtools import _
from ui.custom_widgets import *
import time


Builder.load_file('ui/ddd_widgets.kv')


class I18NObjImageButton(Button):
    model = StringProperty()
    text_source = StringProperty()
    key = StringProperty()

    def start_animations(self):
        self.ids.renderer.start_animations()

    def stop_animations(self):
        self.ids.renderer.stop_animations()


class Renderer(Widget):
    model = StringProperty(allow_none=True)

    def __init__(self, **kwargs):
        self.canvas = RenderContext()
        shader = resource_find('simple.glsl')
        if not shader:
            Logger.error("Shader not found")
        self.canvas.shader.source = shader
        self._running = False
        super(Renderer, self).__init__(**kwargs)

    def start_animations(self):
        Clock.schedule_interval(self.update_glsl, 1 / 60.)
        self._running = True
        self.on_model(self, self.model)

    def stop_animations(self):
        self._running = False
        self.canvas.clear()
        Clock.unschedule(self.update_glsl)

    def on_model(self, instance, value):
        if self._running:
            if value:
                self.canvas.clear()
                self.scene = ObjFile(self.model)
                with self.canvas:
                    self.cb = Callback(self.setup_gl_context)
                    PushMatrix()
                    self.setup_scene()
                    PopMatrix()
                    self.cb = Callback(self.reset_gl_context)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def update_glsl(self, *largs):
        asp = max(self.width / float(self.height),1)
        proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
        
        tx = ((self.center_x / float(Window.width)) * 2.0) - 1.0
        ty = ((self.center_y / float(Window.height)) * 2.0) - 1.0
        trans = Matrix().translate(tx,ty,0)
        self.canvas['projection_mat'] = proj
        self.canvas['diffuse_light'] = (1.0, 1.0, 0.8)
        self.canvas['ambient_light'] = (0.1, 0.1, 0.1)
        self.canvas['translate_mat'] = trans
        self.rot.angle += 1

    def setup_scene(self):
        Color(1, 1, 1, 1)
        PushMatrix()
        Translate(0,0,-3)
        Rotate(15, 1, 0, 0)
        self.rot = Rotate(1, 0, 1, 0)
        m = list(self.scene.objects.values())[0]
        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=m.vertices,
            indices=m.indices,
            fmt=m.vertex_format,
            mode='triangles',
        )
        PopMatrix()
