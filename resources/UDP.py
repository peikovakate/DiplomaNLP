# -*- coding: utf-8 -*-
# UDP - Unsupervised Dependency Parsing
from usurper import soegaard
from usurper.utils.conll import export_to_conll_format
import networkx as nx
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import matplotlib.pyplot as plt
from resources.TextAnalyzer import TextAnalyzer

# sent = "Чиста річка біжить в гарному місті"
sent = "Кут, на який змінюється напрям поширення випромінювання, залежить від оптичної густини обох середовищ"
analyzer = TextAnalyzer(sent)
tokens = analyzer.tokens
print(analyzer.tokens)
tags = analyzer.pos_for_udp()
print(tags)
# tags = [x if x != None else 'X' for x in tags]


function_words = ["задежить"]
ppp = soegaard.parse_sentence(tokens, function_words, False, tags, "uk-oc")

# positions = {0: (1, 1), 4: (2, 2)}
# for x in range(0, 3):
#     positions[x] = (x, x);
# print(positions)
# pos = graphviz_layout(ppp)
# nx.draw_networkx(ppp, with_labels=True, pos=nx.spring_layout(ppp, pos=positions, fixed=[0, 4], center=[0, 4]))
nx.draw_networkx(ppp, with_labels=True)
res = export_to_conll_format(ppp)

for word in res:
    print("\t".join(word))

print(ppp.adj)

plt.show()