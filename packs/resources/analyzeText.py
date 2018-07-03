from packs.resources.TextAnalyzer import TextAnalyzer
from packs.resources.TextAnalyzer import Model
from packs.resources.udp_yara import UDParser
from packs.resources.question_generator import QuestionGenerator
from packs.resources.tools.read_conll import ConllReader


class TestGenerator:

    @staticmethod
    def generate_test(text, is_yara=True):
        """
        generates test for given text
        :param text: string - raw text,
        :return: string - text fo test
        """
        test = ''
        raw = TextAnalyzer.change_apostrophe(text)
        sents = TextAnalyzer.tokenize_sentences(raw, is_tokenize_uk=False)

        # ud_graphs = tokens_list = []
        if is_yara:
            nx_ud_graphs, tokens_list = TestGenerator._graph_with_yara(sents)
        else:
            nx_ud_graphs, tokens_list = TestGenerator._graph_with_udpipe(sents)

        all_tasks = []
        for i in range(len(nx_ud_graphs)):
            questions = QuestionGenerator.subj_question(nx_ud_graphs[i], tokens_list[i])
            all_tasks+=questions
            # questions.append(QuestionGenerator.appos_qustion(nx_ud_graphs[i], tokens_list[i]))
            # if len(questions) == 0:
            #     test += '-'
            # else:
            #     test += '\n'.join(str(q) for q in questions)
            # test += '\n'

        return all_tasks

    @staticmethod
    def _graph_with_yara(sents):
        tokens_list = []
        pos_tags_list = []
        # processing tokenization and POS-tagging
        for sent in sents:
            # tokenizes sentence to words
            tokens = TextAnalyzer.tokenize_words(sent)
            # gets POS tag for every token
            pos_tags = TextAnalyzer.ud_pos_tags(tokens)
            # adds tokens and tags to lists
            tokens_list.append(tokens)
            pos_tags_list.append(pos_tags)

        # getting array of directed graphs, where graph is dependency tree for particular sentences
        nx_ud_graphs = UDParser.parse_sentences(tokens_list, pos_tags_list)
        return nx_ud_graphs, tokens_list

    @staticmethod
    def _graph_with_udpipe(sents):
        tokens_list = []
        text = ''
        for sent in sents:
            sent = TextAnalyzer.change_apostrophe_back(sent)
            tokens = TextAnalyzer.tokenize_words(sent)
            tokens_list.append(tokens)
            # deleting "." from sentences, because Model badly tokenizes sents
            if sent[len(sent)-1] == '.':
                sent = sent.replace('.', '')
                sent+='.'
            else:
                sent = sent.replace('.', '')
            text += sent

        model = Model('ukr/ukrainian-ud-2.0-170801.udpipe')
        sentences = model.tokenize(text)
        for s in sentences:
            model.tag(s)
            model.parse(s)
        conllu = model.write(sentences, "conllu")
        print(conllu)

        # parsec conll trees
        trees = ConllReader.parse_conll_format(conllu)
        nx_graphs = [TextAnalyzer.graph(tree) for tree in trees]
        return nx_graphs, tokens_list


    @staticmethod
    def generate_test_for_file(path):
        f = open(path, encoding='utf-8')
        raw = f.read()

        return TestGenerator.generate_test(raw)
