# -*- coding: utf-8 -*-
"""
Created on Tue Mar 20 11:07:15 2018

@author: peiko
"""

#number of symbols
#number of tokens
#number of sents
#number of types
#number of types to lower??
#freq distr
#number of местоимений?

from TextAnalyzer import TextAnalyzer


f = open("texts/biology.txt");
raw = f.read();

analyzer = TextAnalyzer(raw);

print("number of characters = ", analyzer.text_length());
print("number of tokens = ", analyzer.number_of_tokens());
print("number of types = ", analyzer.number_of_types());
print("number of unique words = ", len(analyzer.unique_words));

print("uknown_words = ", analyzer.uncertain_words());

print("distribution of types: \n ", 
      analyzer.distribution(analyzer.tokens).most_common(30));
print("distribution of lemmatised types: \n ", 
      analyzer.distribution(analyzer.lemmatised_tokens).most_common(30));
     
print("vital tokens distr")
vital_tokens = analyzer.define_vital_types(analyzer.lemmatised_tokens);
print(analyzer.distribution(vital_tokens).most_common(30));


# =============================================================================
# print("all types:");
# print(sorted(analyzer.types));
# =============================================================================
#print("unique words:");
#print(sorted(unique_words));

#analyzer.init_analisys();


