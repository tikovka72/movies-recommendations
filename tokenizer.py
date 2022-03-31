import numpy as np
from pickle import load
from typing import Iterable
from tensorflow.keras.preprocessing.text import Tokenizer


class CustomTokenizer:
    def __init__(self, fp='tokenizer.pickle'):
        with open(fp, 'rb') as f:
            self.tokenizer: Tokenizer = load(f)

    @staticmethod
    def _indexes_to_binary(
            words_indexes: np.array,
            bag_size: int = 8000):
        if not bag_size:
            bag_size = max(words_indexes)
        binary_words = np.zeros(bag_size)
        binary_words[words_indexes] = 1
        return binary_words

    def _get_indexes(self, words: Iterable):
        return self.tokenizer.texts_to_sequences(words)

    def get_binary_indexes(self, words: Iterable):
        return self._indexes_to_binary(self._get_indexes(words))
