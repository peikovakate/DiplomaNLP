# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 22:04:15 2018

@author: peiko
"""

import nltk;
from nltk.book import FreqDist
import tokenize_uk;
import pymorphy2;

class TextAnalyzer:
    vitalPOSs='NOUN VERB ADJS ADVB NUMBER';
    
    def __init__(self, raw):
        self.raw_text = raw;
        
        #changing aposstrophe character for pymorpty2
        self.raw_text = self.change_apostrophe(self.raw_text);
        
        #self.tokens = nltk.word_tokenize(self.raw_text);
        self.tokens = tokenize_uk.tokenize_words(self.raw_text);
        self.types = set(self.tokens);
        self.unique_words = set([w.lower() for w in self.types if w.isalpha()]);
        self.morph_analyzer = pymorphy2.MorphAnalyzer(lang='uk');
        
        self.lemmatised_tokens = self.lemmatise(self.tokens);
    
    def change_apostrophe(self, text):
        return text.replace("’", "'");
         
    def text_length(self):
        return len(self.raw_text);
    
    def number_of_tokens(self):
        return len(self.tokens);
    
    def number_of_types(self):
        return len(self.types);
    
    #finding words where pymorphy2 confidence score < 1
    def uncertain_words(self):
        uncertain_words = [];
        for t in self.types:
            if self.morph_analyzer.parse(t)[0].score < 1:
                uncertain_words.append(t);
        return uncertain_words;
    
    def lemmatise(self, data):
        lemmas = [];
        for t in data:
            lemmas.append(self.morph_analyzer.parse(t)[0].normal_form);
        return lemmas;
        
    
    def distribution(self, data):
        fdist = FreqDist(data);
        return fdist;
    
    
    def define_vital_types(self, data):
        vital_types = []
        for t in data:
            p = self.morph_analyzer.parse(t);
            if len(p)==0:
                print('!!')
            p = p[0];
            if p.tag.POS and p.tag.POS in self.vitalPOSs:
                vital_types.append(t)
        return vital_types;
