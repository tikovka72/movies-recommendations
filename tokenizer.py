from pickle import load


def get_tokenizer(fp='tokenizer.pickle'):
    with open(fp, 'rb') as f:
        tokenizer = load(f)

    return tokenizer
