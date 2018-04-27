import  networkx as nx
class ConllReader:
    # todo: check for multiple trees from parser
    @staticmethod
    def read(file_name):
        trees = []
        file = open(file_name, "r")
        lines = file.readlines()
        file.close()
        lines_of_tree = []

        for line in lines:
            if line is '\n':
                trees.append(ConllReader.split_tree(lines_of_tree))
                lines_of_tree.clear()
            else:
                lines_of_tree.append(line)
        # if we got to the end of files, but the lust sent still in buffer of lines_of_tree
        if len(lines_of_tree) is not 0:
            trees.append(ConllReader.split_tree(lines_of_tree))

        return trees

    @staticmethod
    def split_tree(lines):
        '''takes list of lines that refers to one sentence,
        returns list of description for every word,
        description = list of attributes'''
        tree = []
        for line in lines:
            attributes = line.split("\t")
            # for last attribute there is an additional '\n' sign - end of line, that we get reed of
            attributes[len(attributes)-1] = attributes[len(attributes)-1][:-1]
            tree.append(attributes)
        return tree



