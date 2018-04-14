# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 21:34:07 2018

@author: peiko
"""

from usurper import soegaard
from usurper.utils.conll import export_to_conll_format
import matplotlib.pyplot as plt
import networkx as nx

from TextAnalyzer import TextAnalyzer

sent = "Чиста річка біжить в цьому місті"
analyzer = TextAnalyzer(sent)
tokens = analyzer.tokens
print(analyzer.tokens)
tags = analyzer.posTags()
print(tags)
m = {"NOUN": "NOUN", "VERB": "VERB", "ADJF": "ADJ",
     "ADJS": "ADJ", "ADVB": "ADV", "NPRO": "PRON",
     "PREP": "ADP",
     "CONJ": "CONJ", None: "."}
univTags = []

for t in tags:
    univTags.append(m[t])

print(univTags)
function_words = ()
ppp = soegaard.parse_sentence(tokens, function_words, True, univTags)

nx.draw(ppp, with_labels=True, font_weight='bold', )
print(export_to_conll_format(ppp))
