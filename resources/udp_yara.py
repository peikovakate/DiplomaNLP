from subprocess import check_output
from resources.TextAnalyzer import TextAnalyzer
from resources.tools.read_conll import ConllReader
import logging


class UDParser:
    @staticmethod
    def parse_sentences(sentences, pos_tags):
        """
        writes pos tagged sentences to file, runs YaraParser and parses its output

        :param sentences: list of sentences, where sentences is list of tokens
        :param pos_tags: list of list, where inner list contains POS tags for tokens in 'sentences'
        :return: list of networkx directed graphs
        """

        pos_tagged_sents = UDParser.tag_sentences(sentences, pos_tags)
        UDParser.sents_to_file(pos_tagged_sents)

        command_str = "java -jar ../YaraParser/YaraParser.jar parse_tagged " \
                      "-input ../ukr/text_to_parse.txt -out ../ukr/pos_result -model ../ukr/tr_model_iter20"

        # command_str = "java -jar ../YaraParser/YaraParser.jar parse_conll  " \
                      # "-input ../ukr/text_conll_to_parse.conll -out ../ukr/pos_result -model ../ukr/tr_model_iter20"

        output = check_output(command_str, shell=True).decode(encoding="utf-8")
        # print(output)

        trees = ConllReader.read("../ukr/pos_result")
        graphs = [TextAnalyzer.graph(tree) for tree in trees]
        return graphs

    @staticmethod
    def tag_sentences(sents, ud_tags):
        """returns list of lines (strings) with POS tag after every token, delimiter between token and tag is '_' """
        lines = []
        for t in range(len(sents)):
            tokens = sents[t]
            tags = ud_tags[t]
            # labels = {i + 1: tokens[i] for i in range(0, len(tokens))}
            s = " ".join(tokens[i] + "_" + tags[i] for i in range(0, len(tokens)))
            lines.append(s)
        return lines

    @staticmethod
    def sents_to_file(lines):
        file = open("../ukr/text_to_parse.txt", "w", encoding='utf-8')
        for line in lines:
            file.write(line + '\n')
        file.close()
