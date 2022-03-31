def keywords_to_binary(words_indexes, num_words=8000):
    binary_words = np.zeros(num_words)
    binary_words[words_indexes] = 1
    return binary_words