#!/usr/bin/env python

__version__ = "0.0.1"

import html
import random
import re

import numpy as np
from scipy.sparse import bsr_matrix, coo_matrix, csc_matrix, csr_matrix, dia_matrix, dok_matrix, lil_matrix
from sklearn.preprocessing import normalize




class Xion():

    last_index = 0

    def __init__(self, markov_matrix_size=10000):
        self.markov_matrix = lil_matrix((markov_matrix_size, markov_matrix_size), dtype=np.float32)
        self.words = dict()
        self.start_words = []


    def index(self, word):
        if word in self.words:
            index = self.words[word]
        else:
            self.words[word] = self.last_index
            index = self.last_index
            self.last_index += 1

        return index


    def insert(self, word1, word2):
        index1 = self.index(word1)
        index2 = self.index(word2)
        self.markov_matrix[index1, index2] += 1


    def random_speak(self):

        keys = list(self.words.keys())
        msg = [random.choice(keys)for i in range(10)]
        return ' '.join(msg)


    def speak(self, max_length=140):
        for attempt in range(100):
            toks = []
            N = len(self.words)
            indexes = np.arange(N, dtype=np.int32)
            start_word = random.choice(self.start_words)
            toks.append(start_word)
            idx = self.words[start_word]
            while not toks[-1].endswith('.') and len(toks) < 200:
                weights = self.markov_matrix[idx,:N].A[0]
                if not weights.any():
                    break
                mask = weights > 0
                idx = np.random.choice(indexes[mask], p=weights[mask])
                word = self.idx_to_words[idx]
                toks.append(word)

            msg = ' '.join(toks)
            if len(toks) < 3:
                continue
            if len(msg) > max_length:
                continue
            else:
                return msg
            print(f'attempt: {attempt}')


    def tokenize(self, msg):
        tokens = []

        # remove urls
        # no idea how the (?:) bit works, but it matches space or end of string
        msg = re.sub('http(s)?:.+(?:\s+|$)', '', msg)

        for sentence in msg.strip().split('. '):
            words = sentence.strip().split()
            if len(words) < 2:
                continue

            self.start_words.append(words[0])

            for word in words:
                tokens.append(html.unescape(word))

            if tokens[-1][-1] not in ('!', '?', '.'):
                tokens[-1] += '.'

        return tokens


    def train(self, text):
        last_word = None
        for word in self.tokenize(text):
            if ('http:' in word) or ('https:' in word):
                # skip links
                last_word = None
                continue
            if last_word:
                self.insert(last_word, word)
            last_word = word


    def normalize(self):

        self.markov_matrix = normalize(csr_matrix(self.markov_matrix), norm='l1', axis=1)
        self.idx_to_words = {v: k for k, v in self.words.items()}

