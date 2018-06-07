import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ObjectProperty, StringProperty
kivy.require('1.10.0')


class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

        # self.cols = 3
        # # self.row_force_default = True
        # # self.row_default_height = 40
        # self._input_text = TextInput()
        # self._settings_layout = StackLayout(size_hint_x=None, width=300, orientation='tb-lr')
        # self._output_text = TextInput()
        # self.add_widget(self._input_text)
        # self.add_widget(self._settings_layout)
        # self.add_widget(self._output_text)
    label_wid = ObjectProperty()
    info = StringProperty()

    def do_action(self):
        self.label_wid.text = 'My label after button press'
        self.info = 'New info text'

class TestIT(App):
    icon = 'style/list.png'

    def build(self):
        return MainScreen()


if __name__ == '__main__':
    TestIT().run()