import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.gridlayout import GridLayout

from serial import Serial

class MyButtons(GridLayout):
    def __init__(self, **kwargs):
        super(MyButtons, self).__init__(**kwargs)
        # self._conn = Serial('/dev/ttyACM0')

    def ba(self):
        self.button_hit('a')

    def bb(self):
        self.button_hit('b')

    def bc(self):
        self.button_hit('c')

    def bd(self):
        self.button_hit('d')

    def be(self):
        self.button_hit('e')

    def bf(self):
        self.button_hit('f')

    def button_hit(self, button):
        # self._conn.write(button)
        print 'wrote: %s' % button

class SerialApp(App):
    def build(self):
        return MyButtons(cols=2)


if __name__ == '__main__':
    SerialApp().run()