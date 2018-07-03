import networkx as nx
rules = {'nsubj': ['Що', '_root', '?']}

class Task:
    question_text = ''
    right_answer_text = ''
    right_answer_sign = ''
    possible_answers = {}

    def possible_answers_str(self):
        s = ''
        for variant in self.possible_answers:
            s += str(variant)+': ' + self.possible_answers[variant] + '\n'
        return s

    def printTask(self):
        return "\n".join(str(x) for x in [self.question_text, self.possible_answers_str()])


class QuestionGenerator:


    @staticmethod
    def subj_question(sentence_graph, tokens):
        tokens[0] = tokens[0].lower()
        root = list(sentence_graph[0])[0]
        subjs = QuestionGenerator._get_tokens_indexes_under_relation(sentence_graph, root, "nsubj")
        tasks = []
        for token_ids in subjs:
            ids = sorted(token_ids)
            subj = QuestionGenerator._ids_to_tokens(ids, tokens)
            other_words_ids = set(range(1, len(tokens)))-set(ids)
            question = QuestionGenerator._ids_to_tokens(other_words_ids, tokens)
            question = 'Що ' + question + '?'
            question += ' Відповідь: ' + subj

            task = Task()
            task.question_text = question
            task.right_answer_text = subj

            tasks.append(task)
        return tasks


    @staticmethod
    def _get_sent_part(part_id, sentence_graph, root):
        targets = QuestionGenerator._get_tokens_indexes_under_relation(sentence_graph, root, part_name)
        part_ids = []
        for token_ids in targets:
            ids = sorted(token_ids)
            # target = QuestionGenerator._ids_to_tokens(ids, tokens)
            other_words_ids = set(sentence_graph) - set(ids)
            part_ids.append((ids, other_words_ids))
            # question = QuestionGenerator._ids_to_tokens(other_words_ids, tokens)
            # question = 'Що(хто) ' + question + '?'

            # question += ' Відповідь: ' + target
            # target_sents.append(question)
        return part_ids

    def _get_sent_part(part_name, sentence_graph, root):
        targets = QuestionGenerator._get_tokens_indexes_under_relation(sentence_graph, root, part_name)
        part_ids = []
        for token_ids in targets:
            ids = sorted(token_ids)
            # target = QuestionGenerator._ids_to_tokens(ids, tokens)
            other_words_ids = set(sentence_graph) - set(ids)
            part_ids.append((ids, other_words_ids))
            # question = QuestionGenerator._ids_to_tokens(other_words_ids, tokens)
            # question = 'Що(хто) ' + question + '?'

            # question += ' Відповідь: ' + target
            # target_sents.append(question)
        return part_ids

    @staticmethod
    def target_question(target_name, sentence_graph, tokens, root = 0):
        root = list(sentence_graph[0])[root]
        parts = rules[target_name]
        sent_text = ''
        for part in parts:
            if part[0]!='_':
                sent_text+=part
            else:
                pass

        return target_sents

    @staticmethod
    def appos_qustion(sentence_graph, tokens):
        root = list(sentence_graph[0])[0]
        appos = QuestionGenerator._get_tokens_indexes_under_relation(sentence_graph, root, "appos")
        appos_sents = []
        for token_ids in appos:
            ids = sorted(token_ids)
            subj = QuestionGenerator._ids_to_tokens(ids, tokens)
            other_words_ids = set(range(1, len(tokens)+1))-set(ids)
            question = QuestionGenerator._ids_to_tokens(other_words_ids, tokens)
            question = 'Що(хто) ' + question + '?'
            question += ' ' + subj
            appos_sents.append(question)
        return appos_sents

    @staticmethod
    def _ids_to_tokens(ids, tokens):
        return " ".join(tokens[index-1] for index in ids)

    @staticmethod
    def _get_vertexes_with_relation(graph, parent, relation):
        edges = []
        for child in graph[parent]:
            if graph[parent][child]['relation'] == relation:
                edges.append(child)
        return edges

    @staticmethod
    def _get_nodes_of_subtree(graph, parent):
        tree = nx.bfs_tree(graph, parent)
        return tree.nodes()

    @staticmethod
    def _get_tokens_indexes_under_relation(graph, node, relation):
        '''returns array of lists of tokens id that refer to particular relation to given node'''
        vertexes = QuestionGenerator._get_vertexes_with_relation(graph, node, relation)
        phrases = []
        for vertex in vertexes:
            tokens_id = QuestionGenerator._get_nodes_of_subtree(graph, vertex)
            phrases.append(tokens_id)
        return phrases

    @staticmethod
    def _delete_subtree(parent, child):
        # todo: need implementation
        pass

