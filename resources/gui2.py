import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
kivy.require('1.10.0')
from resources.analyzeText import TestGenerator


class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def generate_test(self):
        raw = self.ids.input_text.text
        result = TestGenerator.generate_test(raw, is_yara=True)
        self.ids.output_text.text = result



class TestIT(App):
    icon = 'style/list.png'
    def build(self):
        return MainScreen()


TestIT().run()


# if __name__ == '__main__':
#     TestIT().run()