import json
import os
import create_dictionary
import numpy as np
class bigram_lm:
    def __init__(self, name = 'corpus'):
        create_dictionary.tok_text(name)
        self.name = name
        self.prob_of_words = {}

        if not os.path.exists('corpus/' + self.name + '_probability_dict.json'):
            print 'saving bigram probability model'
            with open('corpus/' + self.name + '.json', 'r') as corpus:
                self.corpus = json.load(corpus)
            self.dict_unigram_freq = {}
            self.dict_bigram_freq = {}
            self.unigram_freq()
            self.bigram_freq()
            self.prob_of_next_word()
            self.save_prob_dict()
        else:
            print 'loading existing bigram probability model'
            self.load_existing_dictionary()

    def unigram_freq(self):
        for word in self.corpus:
            if self.dict_unigram_freq.has_key(word):
                self.dict_unigram_freq[word] += 1
            else:
                self.dict_unigram_freq[word] = 1

    def bigram_freq(self):
        for bigram in range(len(self.corpus) - 1):

            if (self.corpus[bigram], self.corpus[bigram + 1]) in self.dict_bigram_freq:
                self.dict_bigram_freq[(self.corpus[bigram], self.corpus[bigram + 1])] += 1
            else:
                self.dict_bigram_freq[(self.corpus[bigram], self.corpus[bigram + 1])] = 1


    def prob_of_next_word(self):

        for bigram in self.dict_bigram_freq:
            self.prob_of_words[bigram] = np.log(self.dict_bigram_freq[bigram])- np.log(self.dict_unigram_freq[bigram[0]])

    def save_prob_dict(self):
        dumpbiprob = {}
        for tups in self.prob_of_words:
            dumpbiprob[tups[0] + ' ' + tups[1]] = self.prob_of_words[tups]
        with open('corpus/' + self.name + '_probability_dict.json', 'w') as outfile:
            json.dump(dumpbiprob, outfile)

    def load_existing_dictionary(self):
        with open('corpus/' + self.name + '_probability_dict.json', 'r') as prob_dict:
            unformated_prob_dict = json.load(prob_dict)
        for key in unformated_prob_dict:
            self.prob_of_words[tuple(key.split(' '))] = unformated_prob_dict[key]

    def nextword(self, word):
        word_probs = []
        for prob in self.prob_of_words:
            if prob[0] == word:
                word_probs.append((prob[0], prob[1], self.prob_of_words[prob]))
        return sorted(word_probs, key=lambda tup: tup[2], reverse=True)
