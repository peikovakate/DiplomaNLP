# DiplomaNLP
Master diploma project in NLP

**Topic**: Test generation for ukrainian texts

---
##### Tools and techniques:
* pymorphy2 - dictionary (opencorpora tags, normal form)
* nlp - statistics
* Yara parser - dependency parser https://github.com/yahoo/YaraParser
* networkx - graph library, usage - in code representation for dependency trees
* conll, conllu - formats for dependency trees
http://universaldependencies.org/#language-
* Gold standard Universal Dependencies corpus for Ukrainian
https://github.com/UniversalDependencies/UD_Ukrainian-IU/tree/master

---
##### Notes:
In need of nice tool of converting opencorpora pos tag to universal dependency pos tag
some problems samples:

NPRO	PRON => NPRO	ADJ
PREP	ADP => PREP	PRT