from resources.TextAnalyzer import TextAnalyzer
from resources.udp_yara import UDParser
from resources.question_generator import QuestionGenerator
f = open("../texts/greak_war.txt")
raw = f.read()
raw = TextAnalyzer.change_apostrophe(raw)
sents = TextAnalyzer.tokenize_sentences(raw)
for sent in sents:
    tokens = TextAnalyzer.tokenize_words(sent)
    print(sent)
    pos_tags = TextAnalyzer.ud_pos_tags(tokens)
    ud_graph = UDParser.parse_sentences([tokens], [pos_tags])
    print(QuestionGenerator.subj_question(ud_graph[0], tokens))
    print()


