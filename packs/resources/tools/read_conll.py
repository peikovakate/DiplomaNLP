class ConllReader:
    # todo: check for multiple trees from parser
    @staticmethod
    def read(file_name):

        file = open(file_name, "r")
        text = file.read()
        file.close()
        return ConllReader.parse_conll_format(text)

    @staticmethod
    def read_as_raw(file_name):
        raws = []
        file = open(file_name, "r", encoding='utf-8')
        lines = file.readlines()
        file.close()
        for line in lines:
            if line != '\n' and line[0] != '#':
                raws.append(ConllReader._split_line(line))
        return raws

    @staticmethod
    def parse_conll_format(conll_text):
        lines = conll_text.splitlines()
        trees = []
        lines_of_tree = []
        for line in lines:
            if (line == '\n' or line == '') and lines_of_tree != []:
                trees.append(ConllReader._split_tree(lines_of_tree))
                lines_of_tree.clear()
            if line == '':
                pass
            elif line[0] != '#':
                lines_of_tree.append(line)
        # if we got to the end of files, but the last sent still in buffer of lines_of_tree
        if len(lines_of_tree) != 0:
            trees.append(ConllReader._split_tree(lines_of_tree))
        return trees

    @staticmethod
    def _split_line(line):
        attributes = line.split("\t")
        # for last attribute there is an additional '\n' sign - end of line, that we get reed of
        attributes[len(attributes) - 1] = attributes[len(attributes) - 1][:-1]
        return attributes

    @staticmethod
    def _split_tree(lines):
        '''takes list of lines that refers to one sentence,
        returns list of description for every word,
        description = list of attributes'''
        tree = []
        for line in lines:
            tree.append(ConllReader._split_line(line))
        return tree



