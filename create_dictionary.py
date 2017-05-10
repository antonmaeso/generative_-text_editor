import nltk
import json
import os

class tok_text():
    def __init__(self, name_of_corpus = 'corpus'):
        self.name = name_of_corpus
        self.text = open('corpus/' + self.name + '.txt').read()
        self.text_tok = nltk.casual_tokenize(self.text)
        if not os.path.exists('corpus/' + self.name + '_word_int_dict.json'):
            print 'create dictionaries'
            self.word_to_int = {}
            self.createdict()
            self.int_to_word = {v: k for k, v in self.word_to_int.items()}
            self.save_text_toke()
            self.save_int_to_word_dict()
            self.save_word_to_int_dict()
        else:
            print 'load existing dictionary'
            with open('corpus/' + self.name + '_int_word_dict.json', 'r') as int_word_dict:
                self.int_to_word = json.load(int_word_dict)
            with open('corpus/' + self.name + '_word_int_dict.json', 'r') as word_int_dict:
                self.word_to_int = json.load(word_int_dict)

    def save_text_toke(self):
        with open('corpus/' + self.name + '.json', 'w') as outfile:
            json.dump(self.text_tok, outfile)



    def createdict(self):
        uniquekey = 1
        for key in self.text_tok:
            if not self.word_to_int.has_key(key):
                self.word_to_int[key] = uniquekey
                uniquekey += 1
            if key == len(self.text_tok) - 1:
                self.word_to_int['UNK'] = key +1



    def save_word_to_int_dict(self):
        with open('corpus/' + self.name + '_word_int_dict.json', 'w') as outfile:
            json.dump(self.word_to_int, outfile)

    def save_int_to_word_dict(self):
        with open('corpus/' + self.name + '_int_word_dict.json', 'w') as outfile:
            json.dump(self.int_to_word, outfile)


    def convert_text_to_int(self):
        return [self.word_to_int[x] for x in self.text_tok]

    def convert_int_to_text(self, int_text):
        return [self.int_to_word[x] for x in int_text]

    def look_up_int(self, int_word):
        return self.word_to_int.keys()[self.word_to_int.values().index(int_word)]
