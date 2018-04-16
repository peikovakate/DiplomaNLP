# -*- coding: utf-8 -*-
"""
Created on Fri Mar 23 22:03:36 2018

@author: peiko
"""
import itertools
import pymorphy2
import codecs
import nltk
from nltk import grammar


f = codecs.open("cfg_rules.fcfg", mode= "w", encoding = "utf-8")
f.writelines("XP -> NP\n")
f.writelines("XP -> VP\n")
f.close()

def fix_pymorphy_tags(d):
    if d['POS'] in "NOUN ADJF" and 'number' not in d.keys():
        d['number'] = 'sing'


def parsed_to_dict(p):
    dict = {};
    tags = p.tag;
    if tags.POS != None:
        dict["POS"] = tags.POS;
    if tags.animacy != None:
        dict["animacy"] = tags.animacy;
    if tags.aspect != None:
        dict["animacy"] = tags.animacy;
    if tags.case != None:
        dict["case"] = tags.case;
    if tags.gender != None:
        dict["gender"] = tags.gender;
    if tags.involvement != None:
        dict["involvement"] = tags.involvement;
    if tags.mood != None:
        dict["mood"] = tags.mood;
    if tags.number != None:
        dict["number"] = tags.number;
    if tags.person != None:
        dict["person"] = tags.person;
    if tags.tense != None:
        dict["tense"] = tags.tense;
    if tags.transitivity != None:
        dict["transitivity"] = tags.transitivity;
    if tags.voice != None:
        dict["voice"] = tags.voice;
        
    dict["norm"] = p.normal_form;
    return dict;

def dict_to_string(d):
    str = ''
    for k in d.keys:
        str += k + ":" + d[k]+ " ";
    return str;
        
def transform_parsed_data(parsed):
    d = parsed_to_dict(p);
    fix_pymorphy_tags(d);
    return d;

def add_lexical_productions(dicts):
    
    for d in dicts:
        str = '';
        
    
        

sent = "Людина йде";
tokens = nltk.word_tokenize(sent.lower());
morph = pymorphy2.MorphAnalyzer(lang='uk');
for token in tokens:
    parsed = morph.parse(token);
    print(token);
    for p in parsed:
        print(transform_parsed_data(p));


# =============================================================================
# parser = nltk.load_parser("cfg_rules.fcfg", trace=1, cache=False);
# trees = parse.parse(tokens);
# for tree in trees:
#     print(tree)
# 
# =============================================================================
    
