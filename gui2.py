import kivy
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
kivy.require('1.10.0')
from tkinter import Tk
from tkinter.filedialog import askopenfilename

import networkx as nx
import random
import nltk
import tokenize_uk
import pymorphy2
import collections
import ufal.udpipe
from subprocess import check_output
import logging

from resources.analyzeText import TestGenerator
from resources.TextAnalyzer import TextAnalyzer, Model

from resources.udp_yara import UDParser
from resources.question_generator import QuestionGenerator
from resources.tools.read_conll import ConllReader
from resources.pos_tagger import POSTagger




from gensim.models import KeyedVectors

word_vectors = KeyedVectors.load_word2vec_format('ukr/wordVectors/ubercorpus.lowercased.tokenized.word2vec.300d')
vecs = word_vectors.wv

vital = ['NOUN', 'VERB', 'ADV', 'NUM', 'ADJ', 'CCONJ']

def generate_answers(task):
    choices = [0, 1, 2]
    for i in choices:
        text = ''
        tokens = task.right_answer_text.split(' ')
        pos_tags = TextAnalyzer.ud_pos_tags(tokens)
        for j in range(len(tokens)):
            tag = pos_tags[j]
            word = tokens[j]
            if word in word_vectors.vocab and tag in vital:
                if i < len(vecs.most_similar(word)):
                    text += ' ' + vecs.most_similar(word)[i][0]
                else:
                    text += ' ' + word
            else:
                text += ' ' + word
        task.possible_answers[i] = text
    return task



class MainScreen(FloatLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)

    def generate_test(self):
        raw = self.ids.input_text.text
        result = TestGenerator.generate_test(raw, is_yara=True)
        text_to_output = ''
        for res in result:
            task = generate_answers(res)
            text_to_output += task.printTask() +'\n'
            # text_to_output = res.printTask()+'\n'

        self.ids.output_text.text = text_to_output

    def save_test(self):
        Tk().withdraw()
        filename = askopenfilename()
        if filename != '' :
            f = open(filename, mode='w')
            file_raw = self.ids.input_text.text
            f.write(file_raw)
            f.close()


    def load_file(self):
        Tk().withdraw()
        filename = askopenfilename()
        if filename != '' :
            f = open(filename, mode='r', encoding='utf-8')
            file_raw = f.read()
            self.ids.input_text.text = file_raw
            f.close()



class TestIT(App):
    icon = 'style/list.png'
    def build(self):
        return MainScreen()


# TestIT().run()


if __name__ == '__main__':
    TestIT().run()