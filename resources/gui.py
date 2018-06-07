import pyforms
from pyforms import BaseWidget
from pyforms.controls import ControlTextArea
from pyforms.controls import ControlButton
from pyforms.controls import ControlFile
from pyforms.controls import ControlCheckBoxList
from pyforms.controls import ControlNumber
from resources.analyzeText import TestGenerator
from pyforms.utils.settings_manager import conf
import resources.style.settings as settings
conf+=settings
from resources.TextAnalyzer import Model
# SETTINGS_PRIORITY = 1
# PYFORMS_STYLESHEET = 'resources/style/style.css'
# PYFORMS_STYLESHEET_WINDOWS = 'resources/style/style.css'
class Gui(BaseWidget):
    _input_format = ''

    def __init__(self):
        super(Gui, self).__init__('Test Generator')
        # self.setWindow
        # Definition of the forms fields
        self._raw_text = ControlTextArea('Твій текст', 'Встав або введи свій текст сюди.', visible=False)
        self._file_path = ControlFile('Файл', visible=False)
        self._button = ControlButton('Згенерувати тест')

        self._test = ControlTextArea(readonly=True)
        self._button.value = self._generate_test_click

        self._input_format = ['_file_path', '_raw_text']
        self._input_file_button = ControlButton('Файл', checkable=True)
        self._input_file_button.value = self._input_file_click
        self._input_text_button = ControlButton('Текст', checkable=True)
        self._input_text_button.value = self._input_text_click

        self._generate_test_tab = [(' ', '_button', ' '), '_test']
        self._input_tab = [('_input_file_button', '_input_text_button'),

                           self._input_format, ' ']

        self._test_task_number_control = ControlNumber(label='Кількість тестових завдань')
        self._tests_number_control = ControlNumber(label='Кількість тестових варіантів')
        self._test_types_checkbox = ControlCheckBoxList(label='Типи тестових завдань:')
        self._test_types_checkbox += ('Вибір одного правильного', False)
        self._test_types_checkbox += ('Множинний вибір', False)
        self._test_types_checkbox += ('Бінарне питання', False)
        self._test_types_checkbox += ('Визначити послідовність', False)
        self._settings_tab = [(' ', '_tests_number_control', ' '),
                              (' ', '_test_task_number_control', ' '),
                              '_test_types_checkbox']
        # self.mainmenu = [{'icon': 'resources/style/exam.png'}]

        self.formset = [
            {
                'a:Текст': self._input_tab,
                'c:Налаштування тесту': self._settings_tab,
                'd:Згенеруй тест': self._generate_test_tab,
            },
        ]

    def _generate_test_click(self):
        text = self._raw_text.value
        self._test.value = TestGenerator.generate_test(text)

    def _input_text_click(self):
        self._raw_text.show()
        self._file_path.hide()
        self._input_format = 'text'
        self._input_text_button.checked = True
        self._input_file_button.checked = False

    def _input_file_click(self):
        self._raw_text.hide()
        self._file_path.show()
        self._input_format = 'file'
        self._input_text_button.checked = False
        self._input_file_button.checked = True


pyforms.start_app(Gui, geometry=(600, 200, 600, 400))
# text = 'Органічна еволюція — це процес історичного розвитку живої природи, що являє собою спрямовані зміни організмів, видів, їх співтовариств і біосфери у цілому.'
# print(TestGenerator.generate_test(text))


# # Can be used as
# model = Model('../ukr/ukrainian-ud-2.0-170801.udpipe')
# file = open("../texts/short_text.txt", encoding='utf-8', mode='r')
# text = file.read()
# file.close()
# sentences = model.tokenize(text)
# for s in sentences:
#     model.tag(s)
#     model.parse(s)
# conllu = model.write(sentences, "conllu")
# print(conllu)