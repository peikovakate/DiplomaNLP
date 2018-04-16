import itertools
import matplotlib.pyplot as plt
import networkx as nx
from usurper import soegaard

from usurper.utils import conll
from usurper.utils import tsv


def sentence_graphs_iter(sentences, tagset, conll_format, origid):
    """"""
    if conll_format:
        return ((conll.create_nx_digraph_from_conll(s, tagset, origid=True), sid) for s, sid in sentences)
    else:
        return ((tsv.create_nx_digraph_from_tsv(s, tagset, origid=True), sid) for s, sid in sentences)


def main():
    print("Try to identify function words")
    Corpus = open('../texts/sometext.txt', 'r')

    t = 'uk-oc'
    is_no_rules = False
    function_words = ("Хлопчик", "Паша", "небі")

    print("Parse sentences")
    # reset file pointer
    Corpus.seek(0)
    sents = tsv.sentences_iter(Corpus, return_id=True)
    sent_graphs = sentence_graphs_iter(sents, t, False, origid=True)

    r = map(soegaard.parse_sentence_graph,
            zip(sent_graphs, itertools.repeat(function_words), itertools.repeat(is_no_rules)))

    for parse_tree in r:
        # nx.draw(parse_tree, with_labels=True)
        lines = ["\t".join(l) for l in conll.export_to_conll_format(parse_tree)]
        print("\n".join(lines) + "\n")
        # plt.interactive(False)
        # plt.show()

    print("Done")




if __name__ == "__main__":
    main()
