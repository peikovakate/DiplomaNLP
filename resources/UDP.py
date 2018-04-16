# -*- coding: utf-8 -*-
# UDP - Unsupervised Dependency Parsing
from usurper import soegaard
from usurper.utils.conll import export_to_conll_format
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
from resources.TextAnalyzer import TextAnalyzer

# sent = "Чиста річка біжить в гарному місті"
sent = "Повстання в Греції розпочалося у другій половині березня 1821 року"
analyzer = TextAnalyzer(sent)
tokens = analyzer.tokens
print(analyzer.tokens)
tags = analyzer.posTags()
print(tags)
tags = [x if x != None else 'X' for x in tags]


function_words = ["Повстання", "березня"]
ppp = soegaard.parse_sentence(tokens, function_words, False, tags, "uk-oc")

# positions = {0: (1, 1), 4: (2, 2)}
# for x in range(0, 3):
#     positions[x] = (x, x);
# print(positions)
pos = graphviz_layout(ppp)
# nx.draw_networkx(ppp, with_labels=True, pos=nx.spring_layout(ppp, pos=positions, fixed=[0, 4], center=[0, 4]))
nx.draw_networkx(ppp, pos, with_labels=True)
res = export_to_conll_format(ppp)

for word in res:
    print("\t".join(word))

plt.show()