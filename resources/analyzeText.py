from resources.TextAnalyzer import TextAnalyzer
from resources.udp_yara import UDParser
from resources.question_generator import QuestionGenerator

f = open("../texts/short_text.txt", encoding='utf-8')
raw = f.read()
raw = TextAnalyzer.change_apostrophe(raw)
sents = TextAnalyzer.tokenize_sentences(raw, is_tokenize_uk=True)
tokens_list = []
pos_tags_list = []
for sent in sents:
    tokens = TextAnalyzer.tokenize_words(sent)
    print(sent)
    pos_tags = TextAnalyzer.ud_pos_tags(tokens)
    tokens_list.append(tokens)
    pos_tags_list.append(pos_tags)

ud_graphs = UDParser.parse_sentences(tokens_list, pos_tags_list)
for i in range(len(ud_graphs)):
    print(QuestionGenerator.subj_question(ud_graphs[i], tokens_list[i]))
    print()



