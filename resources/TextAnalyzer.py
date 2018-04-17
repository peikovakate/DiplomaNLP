# from nltk.book import FreqDist
import tokenize_uk
import pymorphy2
import collections


class TextAnalyzer:
    vitalPOSs = 'NOUN VERB ADJS ADVB NUMBER'

    def __init__(self, raw):
        self.raw_text = raw

        # changing aposstrophe character for pymorphy2
        self.raw_text = self.change_apostrophe(self.raw_text)

        # self.tokens = nltk.word_tokenize(self.raw_text)
        self.tokens = tokenize_uk.tokenize_words(self.raw_text)
        self.types = set(self.tokens)
        self.unique_words = set([w.lower() for w in self.types if w.isalpha()])
        self.morph_analyzer = pymorphy2.MorphAnalyzer(lang='uk')

        self.lemmatised_tokens = self.lemmatise(self.tokens)

    def change_apostrophe(self, text):
        return text.replace("’", "'")

    def text_length(self):
        return len(self.raw_text)

    def number_of_tokens(self):
        return len(self.tokens)

    def number_of_types(self):
        return len(self.types)

    # finding words where pymorphy2 confidence score < 1
    def uncertain_words(self):
        uncertain_words = []
        for t in self.types:
            if self.morph_analyzer.parse(t)[0].score < 1:
                uncertain_words.append(t)
        return uncertain_words

    def lemmatise(self, data):
        lemmas = []
        for t in data:
            lemmas.append(self.morph_analyzer.parse(t)[0].normal_form)
        return lemmas

    def distribution(self, data):
        distr = collections.Counter(data);
        return distr

    def posTags(self):
        poss = []
        for token in self.tokens:
            p = self.morph_analyzer.parse(token)
            poss.append(p[0].tag.POS)
        return poss

    def pos_for_udp(self):
        poss = []
        for token in self.tokens:
            if token in ".!?":
                poss.append(".")
            elif token.isnumeric():
                poss.append("NUMR")
            else:
                p = self.morph_analyzer.parse(token)
                tag = p[0].tag.POS
                poss.append(tag if tag is not None else "X")
        return poss



    # todo: rewrite this method
    def define_vital_types(self, data):
        vital_types = []
        for t in data:
            p = self.morph_analyzer.parse(t)
            if len(p) == 0:
                print('!!')
            p = p[0]
            if p.tag.POS and p.tag.POS in self.vitalPOSs:
                vital_types.append(t)
        return vital_types
