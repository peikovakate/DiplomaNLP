# from nltk.book import FreqDist
import nltk
import tokenize_uk
import pymorphy2
import collections
import networkx as nx
from resources.pos_tagger import POSTagger

# todo: fix function words: 'до' -> preposition, however 'як' -> noun


class TextAnalyzer:

    @staticmethod
    def get_parses(tokens):
        morph_analyzer = pymorphy2.MorphAnalyzer(lang='uk')
        parses = []
        for t in tokens:
            parses.append(TextAnalyzer.get_first(morph_analyzer.parse(t)))
        return parses

    @staticmethod
    def tokenize_words(raw, is_tokenize_uk=False):
        """
        uses nltk by default
        if 'is_tokenize_uk' is True, then uses tokenize_uk
        """
        if is_tokenize_uk:
            return tokenize_uk.tokenize_words(raw)
        else:
            return nltk.word_tokenize(raw)

    @staticmethod
    def tokenize_sentences(raw, is_tokenize_uk=False):
        """
        uses nltk by default
        if 'is_tokenize_uk' is True, then uses tokenize_uk
        """
        if is_tokenize_uk:
            return tokenize_uk.tokenize_sents(raw)
        else:
            return nltk.sent_tokenize(raw)

    @staticmethod
    def change_apostrophe(text):
        """vital for nltk tokenization and pymorphy2 parsing"""
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
    def pos_for_udp(tokens):
        '''pos tagging of tokens list using only pymorphy2'''
        morph_analyzer = pymorphy2.MorphAnalyzer(lang='uk')
        poss = []
        for token in tokens:
            if token.isnumeric():
                poss.append("NUMR")
            else:
                p = morph_analyzer.parse(token)
                tag = TextAnalyzer.get_first(p).tag.POS
                poss.append(tag if tag is not None else "X")
        return poss

    # todo: change method logic! it doesn't work at all!!!
    @staticmethod
    def get_first(parses):
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

    @staticmethod
    def graph(conll_sent):
        '''sentence in conll format (list of list) to networkx directed graph'''
        graph = nx.DiGraph()
        for conll_token in conll_sent:
            graph.add_edge(int(conll_token[6]), int(conll_token[0]), {"relation": conll_token[7]})
        return graph

    @staticmethod
    def dict_of_tokens(tokens):
        dict = {}
        dict[0] = 'ROOT'
        for i in range(0, len(tokens)):
            dict[i+1] = tokens[i]
        return dict

    @staticmethod
    def ud_pos_tags(tokens):
        '''universal pos tagging list of tokens using pymorphy2 and custom POSTagger'''
        # TODO: find best model for opencorpora to ud pos tags converting
        opencp_ud = {
            'ADJF': 'ADJ',
            'ADJS': 'ADJ',
            'ADVB': 'ADV',
            'Apro': 'DET',
            'COMP': 'ADV',
            'CONJ': 'CONJ',
            'GRND': 'VERB',
            'INFN': 'VERB',
            'INTJ': 'INTJ',
            'NOUN': 'NOUN',
            'NPRO': 'ADJ',  # npro pron -> npro adj
            'NUMR': 'NUM',
            'NUMB': 'NUM',
            'PART': 'PRCL',
            'PNCT': 'PUNCT',
            'PRCL': 'PART',
            'PREP': 'ADP',
            'PRTF': 'VERB',
            'PRTS': 'VERB',
            'VERB': 'VERB',
            'X': 'PUNCT',
        }

        tags = []
        pos_tagger = POSTagger()
        parser = pymorphy2.MorphAnalyzer(lang='uk')
        for token in tokens:
            t = pos_tagger.most_freq_tag(token.lower())
            if t == '':
                t = parser.parse(token)[0].tag.POS
                if t in opencp_ud:
                    t = opencp_ud[t]
                else:
                    t = 'X'
            tags.append(t)
        return tags
