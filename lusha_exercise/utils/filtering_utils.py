import re

import numpy as np
from spacy.lang.en import English
from nltk.stem import PorterStemmer

NLP = English()


def get_clean_data(descriptions):
    """
    Clean the descriptions from unnecessary data.

    :param descriptions: the companies descriptions.
    """
    return (get_clean_description(description) for description in descriptions)


def get_clean_description(description):
    """
    Return a filtered clean description for the tfidf model.
    """
    data = description.lower()
    data = remove_symbols(data)
    data = remove_url_links(data)
    words = remove_stopwords(data)
    words = remove_short_words(words)
    words = remove_numbers(words)
    return ' '.join(words)


def remove_symbols(data):
    """
    Remove symbols from the data.
    """
    symbols = "!\"#$%&()*+-./:;<=>?@[\]^_`{|}~\n"
    for i in symbols:
        data = np.char.replace(data, i, ' ')
    return data.tolist()


def remove_url_links(data):
    """
    Remove url links from the data
    """
    text = re.sub(r'(http.*?\s)|(http.*?$)', '', data, flags=re.MULTILINE)
    return re.sub(r'(www.*?\s)|(www.*?$)', '', text, flags=re.MULTILINE)


def remove_stopwords(text):
    """
    Remove english stop words from the text.

    :param text: the text to remove stopwords from.
    :type text: str
    :return: the list of the words from the text, filtered from stopwords.
    :rtype: list[str]
    """
    nlp_reader = NLP(text)

    token_list = []
    for token in nlp_reader:
        token_list.append(token.text)
    filtered_sentence = []

    for word in token_list:
        lexeme = NLP.vocab[word]
        if lexeme.is_stop is False:
            filtered_sentence.append(word)
    return filtered_sentence


def remove_short_words(words):
    """
    Remove words with 2 letters or less.
    """
    return [word for word in words if len(word) > 2]


def remove_numbers(words):
    """
    Remove words that are a numeric.
    """
    return [word for word in words if not word.isnumeric()]


def get_stemmer_words(data):
    """
    Return the words as their stemmer value.
    """
    porter_stemmer = PorterStemmer()
    return ' '.join([porter_stemmer.stem(word) for word in data.split(' ')])
