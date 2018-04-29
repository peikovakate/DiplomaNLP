import networkx as nx
class QuestionGenerator:

    @staticmethod
    def subj_question(sentence_graph, tokens):
        root = list(sentence_graph[0])[0]
        subjs = QuestionGenerator.get_tokens_indexes_under_relation(sentence_graph, root, "nsubj")
        subj_sents = []
        for token_ids in subjs:
            ids = sorted(token_ids)
            subj = QuestionGenerator.ids_to_tokens(ids, tokens)
            other_words_ids = set(range(1, len(tokens)+1))-set(ids)
            question = QuestionGenerator.ids_to_tokens(other_words_ids, tokens)
            question = 'Що(хто) ' + question + '?'
            question += ' ' + subj
            subj_sents.append(question)
        return subj_sents

    @staticmethod
    def ids_to_tokens(ids, tokens):
        return " ".join(tokens[index-1] for index in ids)

    @staticmethod
    def get_vertexes_with_relation(graph, parent, relation):
        edges = []
        for child in graph[parent]:
            if graph[parent][child]['relation'] == relation:
                edges.append(child)
        return edges

    @staticmethod
    def get_nodes_of_subtree(graph, parent):
        tree = nx.bfs_tree(graph, parent)
        return tree.nodes()

    @staticmethod
    def get_tokens_indexes_under_relation(graph, node, relation):
        '''returns array of lists of tokens id that refer to particular relation to given node'''
        vertexes = QuestionGenerator.get_vertexes_with_relation(graph, node, relation)
        phrases = []
        for vertex in vertexes:
            tokens_id = QuestionGenerator.get_nodes_of_subtree(graph, vertex)
            phrases.append(tokens_id)
        return phrases

