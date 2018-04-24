from subprocess import check_output

import networkx as nx
import matplotlib.pyplot as plt
from resources.TextAnalyzer import TextAnalyzer

# sent = "Перевірку пройшли декілька дівчат: гарна Маша, розумна Юля, світла Катя."
sent = "Вони вважали: жива природа розвивається у часі, організми виникли з неорганічних речовин, а види здатні змінюватися."
sent = "Перший елемент, що вибирається в підмножину з множини, може входити, а може і не входити в підмножину, що будується"
sent = "в одному селищі цирульника зобов'язали голити всіх тих мешканців і тільки тих, які не голяться самі"
analyzer = TextAnalyzer(sent)
tokens = analyzer.tokens
print(analyzer.tokens)
tags = analyzer.pos_for_udp()
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

print(tags)
ud_tags = [opencp_ud[t] for t in tags]
print(ud_tags)
# tags = [x if x != None else 'X' for x in tags]

labels = {i+1:tokens[i] for i in range(0,len(tokens))}
print(labels)

file = open("../ukr/text_to_parse.txt", "w")
s = " ".join(tokens[i]+"_"+ud_tags[i] for i in range(0, len(tokens)))
print(s)
file.write(s)
file.close()
command_str = "java -jar ../YaraParser/YaraParser.jar parse_tagged -input ../ukr/text_to_parse.txt -out ../ukr/pos_result -model ../ukr/tr_model_iter20"
print(check_output(command_str, shell=True).decode(encoding="cp1251"))