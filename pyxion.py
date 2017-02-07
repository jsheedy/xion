#!/usr/bin/env python

import numpy as np
import random
import json

class Word(): pass

class Xion():

    last_index = 0
    SIZE = 20000
    markov_matrix = np.zeros((SIZE, SIZE), dtype=np.float16)
    words = dict()

    def index(self, word):
        if word in self.words:
            index = self.words[word]
        else:
            self.words[word] = self.last_index
            self.last_index += 1
            index = self.last_index

        return index

    def insert(self, word1, word2):
        index1 = self.index(word1)
        index2 = self.index(word2)
        self.markov_matrix[index1, index2] += 1

    def speak(self):

        keys = list(self.words.keys())
        msg = [random.choice(keys)for i in range(10)]
        return ' '.join(msg)


comms = '/Users/velotron/project/arise/git/arise/comms/comms.json'

data = json.load(open(comms))


def tokenize(msg):
    tokens = []
    for sentence in msg.split('.'):
        for word in sentence.split():
            tokens.append(word)
    return tokens


xion = Xion()

# "body":"public float Phi() { return (1 + Mathf.Sqrt(5)) / 2; }\n","subject":"best Unity C# function ever written","datetime":"2017-01-31 21:38:00","id":676,"name":"anatomecha"}
for record in data:
    last_word = None
    body = record['body']
    subject = record['subject']
    for word in tokenize(body):
        if last_word:
            xion.insert(word, last_word)
        last_word = word

print(xion.speak())