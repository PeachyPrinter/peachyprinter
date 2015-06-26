from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.button import Button

from infrastructure.object_loader import ObjFile
from infrastructure.langtools import _
from ui.custom_widgets import *
import time


Builder.load_file('ui/ddd_widgets.kv')


class I18NObjImageButton(Button):
    model = StringProperty()
    text_source = StringProperty()
    key = StringProperty()


class Renderer(Widget):
    model = StringProperty(allow_none=True)

    def __init__(self, **kwargs):
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = 'resources/shaders/simple.glsl'
        self.last_update = 0
        super(Renderer, self).__init__(**kwargs)

    def on_model(self, instance, value):
        self.last_update = time.time()
        Clock.unschedule(self.update_glsl)
        if value:
            self.canvas.clear()
            self.scene = ObjFile(self.model)
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
        if time.time() > self.last_update + 100:
            self.on_model(self, self.model)
        else:
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
        m = list(self.scene.objects.values())[0]
        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=m.vertices,
            indices=m.indices,
            fmt=m.vertex_format,
            mode='triangles',
        )
        PopMatrix()
