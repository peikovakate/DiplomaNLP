# from nltk.book import FreqDist
import tokenize_uk
import pymorphy2
import collections

# todo: fix function words: 'до' -> preposition, however 'як' -> noun


class TextAnalyzer:
    vitalPOSs = 'NOUN VERB ADJS ADVB NUMB'

    def __init__(self, raw):
        self.raw_text = raw

        # changing aposstrophe character for pymorphy2
        self.raw_text = self.change_apostrophe(self.raw_text)

        # self.tokens = nltk.word_tokenize(self.raw_text)
        self.tokens = tokenize_uk.tokenize_words(self.raw_text)
        self.types = set(self.tokens)
        self.unique_words = set([w.lower() for w in self.types if w.isalpha()])
        self.morph_analyzer = pymorphy2.MorphAnalyzer(lang='uk')
        self.parses = self.get_parses(self.tokens)
        self.lemmatised_tokens = self.lemmatise()


    def get_parses(self, tokens):
        parses = []
        for t in tokens:
            parses.append(self.get_most_used(self.morph_analyzer.parse(t)))

        return parses

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

    def lemmatise(self, data=None):
        lemmas = []
        parses = []
        if data is None:
            parses = self.parses
        else:
            parses = self.get_parses(data)
        for t in parses:
            lemmas.append(t.normal_form)
        return lemmas

    def distribution(self, data):
        distr = collections.Counter(data)
        return distr

    def posTags(self, tokens=None):
        if tokens is None:
            return [p.tag.POS for p in self.parses]
        else:
            return [p.tag.POS for p in self.get_parses(tokens)]
        return poss

    def pos_for_udp(self):
        poss = []
        for token in self.tokens:
            if token.isnumeric():
                poss.append("NUMR")
            else:
                p = self.morph_analyzer.parse(token)
                tag = self.get_most_used(p).tag.POS
                poss.append(tag if tag is not None else "X")
        return poss

    # todo: change method logic! it doesn't work at all!!!
    def get_most_used(self, parses):

        return parses[0]

        dictionaryAnalyzer_parses = []
        for p in parses:
            if len(p.methods_stack[0]) is 4:
                dictionaryAnalyzer_parses.append(p)

        if len(dictionaryAnalyzer_parses) < 1:
            return parses[0]

        mn = max([p.methods_stack[0][2] for p in dictionaryAnalyzer_parses])
        for p in dictionaryAnalyzer_parses:
            if p.methods_stack[0][2] is mn:
                return p
        return parses[0]

    def define_vital_types(self, tokens=None):
        vital_types = []
        parses = []
        if tokens is None:
            parses = self.parses
        else:
            parses = self.get_parses(tokens)
        for p in parses:
            if p.tag.POS and p.tag.POS in self.vitalPOSs:
                vital_types.append(p.word)
        return vital_types
