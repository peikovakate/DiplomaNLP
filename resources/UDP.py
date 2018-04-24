# -*- coding: utf-8 -*-
# UDP - Unsupervised Dependency Parsing
from usurper import soegaard
from usurper.utils.conll import export_to_conll_format
import networkx as nx
import matplotlib.pyplot as plt
from resources.TextAnalyzer import TextAnalyzer

def hierarchy_pos(G, root, width=1., vert_gap = 0.2, vert_loc = 0, xcenter = 0.5,
                  pos = None, parent = None):
    '''If there is a cycle that is reachable from root, then this will see infinite recursion.
       G: the graph
       root: the root node of current branch
       width: horizontal space allocated for this branch - avoids overlap with other branches
       vert_gap: gap between levels of hierarchy
       vert_loc: vertical location of root
       xcenter: horizontal location of root
       pos: a dict saying where all nodes go if they have been assigned
       parent: parent of this branch.'''
    if pos == None:
        pos = {root:(xcenter,vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    neighbors = G.neighbors(root)
    # if parent != None:   #this should be removed for directed graphs.
    #     neighbors.remove(parent)  #if directed, then parent not in neighbors.
    if len(neighbors)!=0:
        dx = width/len(neighbors)
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = hierarchy_pos(G,neighbor, width = dx, vert_gap = vert_gap,
                                vert_loc = vert_loc-vert_gap, xcenter=nextx, pos=pos,
                                parent = root)
    return pos

class UDP:
    def parse(self, pos_tags, function_words):
        dep_graph = soegaard.parse_sentence(tokens, function_words, False, tags, "uk-oc")
        return dep_graph

    def show_graph(self, graph):
        nx.draw_networkx(self.dep_graph, with_labels=True)
        plt.show()

    def graph_to_string(self, graph):
        return export_to_conll_format(graph)


labels = {}

sent = "Перевірку пройшли декілька дівчат: гарна Маша, розумна Юля, світла Катя."
# sent = "Вони вважали: жива природа розвивається у часі, організми виникли з неорганічних речовин, а види здатні змінюватися."
# sent = "Перший елемент, що вибирається в підмножину з множини, може входити, а може і не входити в підмножину, що будується"
# sent = "в одному селищі цирульника зобов'язали голити всіх тих мешканців і тільки тих, які не голяться самі"
analyzer = TextAnalyzer(sent)
tokens = analyzer.tokens
print(analyzer.tokens)
tags = analyzer.pos_for_udp()
print(tags)
# tags = [x if x != None else 'X' for x in tags]

labels = {i+1:tokens[i] for i in range(0,len(tokens))}
print(labels)

function_words = []
# function_words = ["на", "від", "що", "i", "у", "які", "в", "не", "та"]
ppp = soegaard.parse_sentence(tokens, function_words, False, tags, "uk-oc")
pos = hierarchy_pos(ppp, 0)
# positions = {0: (1, 1), 4: (2, 2)}
# for x in range(0, 3):
#     positions[x] = (x, x);
# print(positions)
# pos = graphviz_layout(ppp)
# nx.draw_networkx(ppp, with_labels=True, pos=nx.spring_layout(ppp, pos=positions, fixed=[0, 4], center=[0, 4]))

nx.draw_networkx(ppp, pos=pos, with_labels=True, labels=labels)
res = export_to_conll_format(ppp)

for word in res:
    print("\t".join(word))

print(ppp.adj)

plt.show()