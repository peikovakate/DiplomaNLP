import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
kivy.require('1.10.0')


class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)


class TestIT(App):
    icon = 'style/list.png'

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    TestIT().run()