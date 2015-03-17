import kivy
kivy.require('1.8.0')
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

from serial import Serial

class MyButtons(BoxLayout):

    txt_log = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(MyButtons, self).__init__(**kwargs)
        self.next_serial_port = 0
        self._conn = None

    def next_serial(self):
        if self._conn:
            self._conn.close()
        try:
            self._conn = Serial(self.next_serial_port)
            new_text = 'Serial port: %s, Name: %s\n' % (self.next_serial_port, self._conn.name)
        except Exception as ex:
            new_text = str(ex) + '\n'
        finally:
            self.next_serial_port += 1
            self.txt_log.text += new_text

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
        if self._conn:
            self._conn.write(button)
            print 'wrote: %s' % button
        else:
            print ' no connection'

class SerialApp(App):
    def build(self):
        return MyButtons(cols=2)


if __name__ == '__main__':
    SerialApp().run()