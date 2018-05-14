from resources.TextAnalyzer import TextAnalyzer
from resources.udp_yara import UDParser
from resources.question_generator import QuestionGenerator


class TestGenerator:

    @staticmethod
    def generate_test(text):
        """
        generates test for given text
        :param text: string - raw text,
        :return: string - text fo test
        """
        test = ''
        raw = TextAnalyzer.change_apostrophe(text)
        sents = TextAnalyzer.tokenize_sentences(raw, is_tokenize_uk=True)
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
        ud_graphs = UDParser.parse_sentences(tokens_list, pos_tags_list)

        for i in range(len(ud_graphs)):
            questions = QuestionGenerator.subj_question(ud_graphs[i], tokens_list[i]);
            if len(questions) == 0:
                test += '-'
            else:
                test += '\n'.join(str(q) for q in questions)
            test += '\n'
        return test

    @staticmethod
    def generate_test_for_file(path):
        f = open(path, encoding='utf-8')
        raw = f.read()

        return TestGenerator.generate_test(raw)


file = "../texts/short_text.txt"
print(TestGenerator.generate_test_for_file(file))







