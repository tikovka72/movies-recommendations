import numpy as np
from pickle import load
from typing import Iterable
from tensorflow.keras.preprocessing.text import Tokenizer


class CustomTokenizer:
    def __init__(self, fp: str = 'tokenizer.pickle',
                 splitter: str = ';',
                 bag_size: int = 8000):
        with open(fp, 'rb') as f:
            self.tokenizer: Tokenizer = load(f)

        self.splitter = splitter
        self.bag_size = bag_size

    def _indexes_to_binary(self, words_indexes: np.array) -> np.array:
        binary_words = np.zeros(self.bag_size if self.bag_size
                                else max(words_indexes))

        binary_words[words_indexes] = 1
        return binary_words

    def _get_indexes(self, words: Iterable) -> np.array:
        return np.array(filter(bool,
                               self.tokenizer.texts_to_sequences(words))
                        ).flatten()

    def get_binary_indexes(self, words: Iterable) -> np.array:
        return self._indexes_to_binary(self._get_indexes(words))

    def cut_words(self, words: str) -> list:
        return words.split(self.splitter)
