import json
import os
import create_dictionary
import numpy as np
class bigram_lm:
    def __init__(self, name = 'corpus'):
        create_dictionary.tok_text(name)
        self.name = name
        self.prob_of_words_bigram = {}
        self.prob_of_words_trigram = {}

        if not os.path.exists('corpus/' + self.name + '_tri_probability_dict.json'):
            print 'saving n-gram probability model'
            with open('corpus/' + self.name + '.json', 'r') as corpus:
                self.corpus = json.load(corpus)
            self.dict_unigram_freq = {}
            self.dict_bigram_freq = {}
            self.dict_trigram_freq = {}
            self.unigram_freq()
            self.bigram_freq()
            self.trigram_freq()
            self.prob_of_next_word_bigram()
            self.prob_of_next_word_trigram()
            self.save_prob_dict()
        else:
            print 'loading existing n-gram probability model'
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

    def trigram_freq(self):
        for trigram in range(len(self.corpus) - 2):

            if (self.corpus[trigram], self.corpus[trigram + 1] + self.corpus[trigram + 2]) in self.dict_trigram_freq:
                self.dict_trigram_freq[(self.corpus[trigram], self.corpus[trigram + 1], self.corpus[trigram + 2])] += 1
            else:
                self.dict_trigram_freq[(self.corpus[trigram], self.corpus[trigram + 1], self.corpus[trigram + 2])] = 1


    def prob_of_next_word_bigram(self):
        for bigram in self.dict_bigram_freq:
            self.prob_of_words_bigram[bigram] = np.log(self.dict_bigram_freq[bigram])- np.log(self.dict_unigram_freq[bigram[0]])

    def prob_of_next_word_trigram(self):
        for trigram in self.dict_trigram_freq:
            self.prob_of_words_trigram[trigram] = np.log(self.dict_trigram_freq[trigram])- np.log(self.dict_bigram_freq[trigram[0],trigram[1]])

    def save_prob_dict(self):
        dumptriprob = {}
        for tups in self.prob_of_words_trigram:
            dumptriprob[tups[0] + ' ' + tups[1] + ' ' + tups[2]] = self.prob_of_words_trigram[tups]
        with open('corpus/' + self.name + '_tri_probability_dict.json', 'w') as outfile:
            json.dump(dumptriprob, outfile)
        outfile.close()
        dumpbiprob = {}

        for tups in self.prob_of_words_bigram:
            dumpbiprob[tups[0] + ' ' + tups[1]] = self.prob_of_words_bigram[tups]
        with open('corpus/' + self.name + '_bi_probability_dict.json', 'w') as outfile:
            json.dump(dumpbiprob, outfile)
        outfile.close()

    def load_existing_dictionary(self):

        with open('corpus/' + self.name + '_bi_probability_dict.json', 'r') as prob_dict:
            unformated_prob_dict = json.load(prob_dict)
        for key in unformated_prob_dict:
            self.prob_of_words_bigram[tuple(key.split(' '))] = unformated_prob_dict[key]

        with open('corpus/' + self.name + '_tri_probability_dict.json', 'r') as prob_dict:
            unformated_prob_dict = json.load(prob_dict)
        for key in unformated_prob_dict:
            self.prob_of_words_trigram[tuple(key.split(' '))] = unformated_prob_dict[key]

    def nextword(self, first_word = None, second_word = None):
        word_probs = []
        if first_word != None and second_word != None:
            for prob in self.prob_of_words_trigram:
                if prob[0] == first_word and prob[1] == second_word:
                    word_probs.append((prob[0], prob[1], prob[2], self.prob_of_words_trigram[prob]))
            sorted_words = sorted(word_probs, key=lambda tup: tup[2], reverse=True)
            return sorted_words
        if first_word != None:
            for prob in self.prob_of_words_bigram:
                if prob[0] == first_word:
                    word_probs.append((prob[0], prob[1], self.prob_of_words_bigram[prob]))
            sorted_words = sorted(word_probs, key=lambda tup: tup[2], reverse=True)
            return sorted_words