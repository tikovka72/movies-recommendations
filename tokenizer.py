from difflib import SequenceMatcher

import numpy as np
from pickle import load
from typing import Iterable

from functools import lru_cache

import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer


class CustomTokenizer:
    MIN_RATIO = 0.8

    def __init__(self, fp: str = 'tokenizer.pickle',
                 splitter: str = ';',
                 bag_size: int = 8000):
        with open(fp, 'rb') as f:
            self.tokenizer: Tokenizer = load(f)

        self.splitter = splitter
        self.bag_size = bag_size

        all_words = [''] + list(map(lambda x: x[1], sorted(
            tuple(self.tokenizer.index_word.items()),
            key=lambda x: x[0])))

        self.all_words = np.array(all_words, dtype=str)

    def _indexes_to_binary(self, words_indexes: np.array) -> np.array:
        binary_words = np.zeros(self.bag_size if self.bag_size
                                else max(words_indexes))

        binary_words[words_indexes] = 1
        return binary_words

    def _get_indexes(self, words: Iterable) -> np.array:
        return np.array(
            tuple(filter(
                lambda index: index != -1,
                map(lambda w: w[0] if len(w) else -1,
                    self.tokenizer.texts_to_sequences(words))))) \
            .flatten().astype(int)

    def get_binary_indexes(self, words: Iterable,
                           need_similar: bool = True) -> np.array:
        indexes = self._get_indexes(words)
        if need_similar:
            indexes = self._get_similar_words(indexes)
        return self._indexes_to_binary(indexes)

    def cut_words(self, words: str) -> list:
        return words.split(self.splitter)

    def _get_similar_words(self, indexes: np.array) -> np.array:
        @lru_cache(maxsize=1024)
        def get_similar_word(word_index: int) -> np.array:
            return np.array(
                [int(SequenceMatcher(
                    None, self.all_words[word_index],
                    self.all_words[temp_index])
                     .ratio() > self.MIN_RATIO)

                 for temp_index in range(self.bag_size)])

        similar_words = np.zeros(self.bag_size)

        for index in indexes:
            similar_words += get_similar_word(index)
        return np.where(similar_words > 0)


def testing_similar_words():
    df = pd.read_csv('csv/movies.csv')
    keywords = df['keywords'].dropna()
    my_tokenizer = CustomTokenizer()
    keywords = my_tokenizer.cut_words(keywords[0])
    indexes1 = np.sort(my_tokenizer._get_indexes(keywords))
    indexes2 = np.sort(
        np.where(my_tokenizer.get_binary_indexes(keywords, True) > 0)[
            0])
    max_len_indexes1 = len(my_tokenizer.tokenizer.index_word[
                               max(indexes1,
                                   key=lambda x: len(
                                       my_tokenizer.tokenizer.index_word[
                                           x]))])

    for i in indexes1:
        word = my_tokenizer.tokenizer.index_word[i]
        print(word, ' ' * (max_len_indexes1 - len(word)), word)

    for i in indexes2:
        if i in indexes1:
            continue
        print(' ' * (max_len_indexes1 + 1),
              my_tokenizer.tokenizer.index_word[i].strip())
