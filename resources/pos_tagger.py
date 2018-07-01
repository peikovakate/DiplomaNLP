from resources.tools.read_conll import ConllReader

class POSTagger:
    def __init__(self, model_file='ukr/pos_model'):
        self.dictionary = {}
        self.model_file = model_file
        self.load_model()

    def load_model(self):
        self.dictionary.clear()
        file = open(self.model_file, 'r', encoding='utf-8')
        lines = file.readlines()
        for line in lines:
            attributes = line.split('\t')
            attributes[len(attributes)-1] = attributes[len(attributes)-1][:-1]
            word = attributes[0]
            self.dictionary[word]={}
            for attr in attributes[1:]:
                pos, freq = attr.split('_')
                self.dictionary[word][pos] = int(freq)
        file.close()

    def pos_tags(self, word):
        word.lower()
        if word in self.dictionary:
            return self.dictionary[word]
        else:
            return {}

    def most_freq_tag(self, word):
        frequencies = self.pos_tags(word)
        max_freq = 0
        m_tag = ''  # tag that has maximum frequency
        for tag in frequencies:
            if max_freq < frequencies[tag]:
                m_tag = tag
                max_freq = frequencies[tag]
        return m_tag


    @staticmethod
    def train(file_name, file_output):
        '''takes conll file'''
        conll_tagged = ConllReader.read_as_raw(file_name)
        dict = {}
        for raw in conll_tagged:
            word = raw[1].lower()
            pos_tag = raw[3]
            if word in dict:
                if pos_tag in dict[word]:
                    dict[word][pos_tag] += 1
                else:
                    dict[word][pos_tag] = 1
            else:
                dict[word] = {}
                dict[word][pos_tag] = 1
        POSTagger.write_trained(file_output, dict)

    @staticmethod
    def write_trained(file_output, trained_dictionary):
        file = open(file_output, 'w', encoding='utf-8')
        for word in trained_dictionary:
            string = word + '\t'
            string += '\t'.join(key+'_'+str(trained_dictionary[word][key]) for key in trained_dictionary[word])
            string += '\n'
            file.write(string)
        file.close()

# POSTagger.train('../ukr/train.conll', '../ukr/pos_model')
