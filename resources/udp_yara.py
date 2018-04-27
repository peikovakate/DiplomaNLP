from subprocess import check_output

import networkx as nx
import matplotlib.pyplot as plt
from resources.TextAnalyzer import TextAnalyzer
from resources.read_conll import ConllReader

def sents_to_file(lines):
    file = open("../ukr/text_to_parse.txt", "w")
    for line in lines:
        file.write(line+'\n')
    file.close()

def sents_to_word_POS(sents):
    opencp_ud = {
        'ADJF': 'ADJ',
        'ADJS': 'ADJ',
        'ADVB': 'ADV',
        'Apro': 'DET',
        'COMP': 'ADV',  # FIXME: it can be ADJ as well, not enough info
        # in OpenCorpora tag
        'CONJ': 'CONJ',
        'GRND': 'VERB',
        'INFN': 'VERB',
        'INTJ': 'INTJ',
        'NOUN': 'NOUN',
        'NPRO': 'PRON',
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
    lines = []
    for sent in sents:
        tokens = TextAnalyzer.tokenize_words(sent)
        tags = TextAnalyzer.pos_for_udp(tokens)
        ud_tags = [opencp_ud[t] for t in tags]
        # labels = {i + 1: tokens[i] for i in range(0, len(tokens))}
        s = " ".join(tokens[i] + "_" + ud_tags[i] for i in range(0, len(tokens)))
        lines.append(s)
    return lines


sent = "Повстання в Греції розпочалося у другій половині березня 1821 року."
text = "Перевірку пройшли декілька дівчат: гарна Маша, розумна Юля, світла Катя. " \
       "Вони вважали: жива природа розвивається у часі, організми виникли з неорганічних речовин, а види здатні змінюватися. " \
       "Перший елемент, що вибирається в підмножину з множини, може входити, а може і не входити в підмножину, що будується."

# sent2 = "Вони вважали: жива природа розвивається у часі, організми виникли з неорганічних речовин, а види здатні змінюватися."
# sent3 = "Перший елемент, що вибирається в підмножину з множини, може входити, а може і не входити в підмножину, що будується"
# sent4 = "в одному селищі цирульника зобов'язали голити всіх тих мешканців і тільки тих, які не голяться самі"

sents = TextAnalyzer.tokenize_sentences(sent)
pos_tagged_sents = sents_to_word_POS(sents)
sents_to_file(pos_tagged_sents)

command_str = "java -jar ../YaraParser/YaraParser.jar parse_tagged " \
              "-input ../ukr/text_to_parse.txt -out ../ukr/pos_result -model ../ukr/tr_model_iter20"
print(check_output(command_str, shell=True).decode(encoding="cp1251"))

trees = ConllReader.read("../ukr/pos_result")

for tree in trees:
    print("tree:")
    print("\n".join('\t'.join(w) for w in tree))
