class ConllReader:
    # todo: check for multiple trees from parser
    @staticmethod
    def read(file_name):
        trees = []
        file = open(file_name, "r", encoding='utf-8')
        lines = file.readlines()
        file.close()
        lines_of_tree = []

        for line in lines:
            if line == '\n':
                trees.append(ConllReader.split_tree(lines_of_tree))
                lines_of_tree.clear()
            elif line[0] != '#':
                lines_of_tree.append(line)
        # if we got to the end of files, but the lust sent still in buffer of lines_of_tree
        if len(lines_of_tree) != 0:
            trees.append(ConllReader.split_tree(lines_of_tree))

        return trees

    @staticmethod
    def read_as_raw(file_name):
        raws = []
        file = open(file_name, "r", encoding='utf-8')
        lines = file.readlines()
        file.close()
        for line in lines:
            if line != '\n' and line[0] != '#':
                raws.append(ConllReader.split_line(line))
        return raws

    @staticmethod
    def split_line(line):
        attributes = line.split("\t")
        # for last attribute there is an additional '\n' sign - end of line, that we get reed of
        attributes[len(attributes) - 1] = attributes[len(attributes) - 1][:-1]
        return attributes

    @staticmethod
    def split_tree(lines):
        '''takes list of lines that refers to one sentence,
        returns list of description for every word,
        description = list of attributes'''
        tree = []
        for line in lines:
            tree.append(ConllReader.split_line(line))
        return tree



