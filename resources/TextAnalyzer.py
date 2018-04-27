# from nltk.book import FreqDist
import tokenize_uk
import pymorphy2
import collections

# todo: fix function words: 'до' -> preposition, however 'як' -> noun


class TextAnalyzer:

    def __init__(self, raw):
        self.raw_text = raw

        # changing aposstrophe character for pymorphy2
        self.raw_text = self.change_apostrophe(self.raw_text)

        # self.tokens = nltk.word_tokenize(self.raw_text)
        self.tokens = self.tokenize_words(self.raw_text)
        self.types = set(self.tokens)
        self.unique_words = set([w.lower() for w in self.types if w.isalpha()])

        self.parses = self.get_parses(self.tokens)
        self.lemmatised_tokens = self.lemmatise()

    @staticmethod
    def get_parses(tokens):
        morph_analyzer = pymorphy2.MorphAnalyzer(lang='uk')
        parses = []
        for t in tokens:
            parses.append(TextAnalyzer.get_most_used(morph_analyzer.parse(t)))

        return parses

    @staticmethod
    def tokenize_words(raw):
        return tokenize_uk.tokenize_words(raw)

    @staticmethod
    def tokenize_sentences(raw):
        return tokenize_uk.tokenize_sents(raw)

    @staticmethod
    def change_apostrophe(text):
        return text.replace("’", "'")

    @staticmethod
    def text_length(raw_text):
        return len(raw_text)

    @staticmethod
    def lemmatise(tokens):
        lemmas = []
        parses = TextAnalyzer.get_parses(tokens)
        for t in parses:
            lemmas.append(t.normal_form)
        return lemmas

    @staticmethod
    def distribution(data):
        distr = collections.Counter(data)
        return distr

    @staticmethod
    def posTags(tokens):
        return [p.tag.POS for p in TextAnalyzer.get_parses(tokens)]

    @staticmethod
    def pos_for_udp(tokens):
        morph_analyzer = pymorphy2.MorphAnalyzer(lang='uk')
        poss = []
        for token in tokens:
            if token.isnumeric():
                poss.append("NUMR")
            else:
                p = morph_analyzer.parse(token)
                tag = TextAnalyzer.get_most_used(p).tag.POS
                poss.append(tag if tag is not None else "X")
        return poss

    # todo: change method logic! it doesn't work at all!!!
    @staticmethod
    def get_most_used(parses):

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

    @staticmethod
    def define_vital_types(tokens):
        vitalPOSs = 'NOUN VERB ADJS ADVB NUMB'
        vital_types = []
        parses = TextAnalyzer.get_parses(tokens)
        for p in parses:
            if p.tag.POS and p.tag.POS in vitalPOSs:
                vital_types.append(p.word)
        return vital_types
