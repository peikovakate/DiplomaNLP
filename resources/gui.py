import pyforms
from pyforms import BaseWidget
from pyforms.controls import ControlTextArea
from pyforms.controls import ControlButton
from pyforms.controls import ControlFile
from resources.analyzeText import TestGenerator


class SimpleExample1(BaseWidget):

    def __init__(self):
        super(SimpleExample1, self).__init__('Simple example 1')

        # Definition of the forms fields
        self._raw_text = ControlTextArea('Твій текст', 'Встав або введи свій текст сюди.')
        self._file_path = ControlFile('Файл')
        self._button = ControlButton('Згенерувати тест')
        self._test = ControlTextArea(readonly=True)
        self._button.value = self._generate_test_click
        self.formset = [
            {
                'a:Встав текст': ['_raw_text'],
                'b:Вибери файл': ['_file_path']

            },
            '=',
            (' ', '_button', ' '),
            '_test'

        ]

    def _generate_test_click(self):
        text = self._raw_text.value
        self._test.value = TestGenerator.generate_test(text)


pyforms.start_app(SimpleExample1, geometry=(600, 200, 600, 800))
# text = 'Органічна еволюція — це процес історичного розвитку живої природи, що являє собою спрямовані зміни організмів, видів, їх співтовариств і біосфери у цілому.'
# print(TestGenerator.generate_test(text))
