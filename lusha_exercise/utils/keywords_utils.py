from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from lusha_exercise.utils.filtering_utils import get_stemmer_words

NUM_OF_KEYWORDS = 5


def create_model(descriptions):
    """
    Create tfidf the model for keyword matching, from the companies description.
    """
    descriptions = [get_stemmer_words(description) for description in descriptions]
    count_vectorizer = CountVectorizer(max_df=0.85, max_features=10000)
    word_count_vector = count_vectorizer.fit_transform(descriptions)
    tfidf_transformer = TfidfTransformer(smooth_idf=True, use_idf=True)
    tfidf_transformer.fit(word_count_vector)
    return count_vectorizer, tfidf_transformer


def sort_coo(coo_matrix):
    """
    Sort the coo metrix.
    """
    tuples = zip(coo_matrix.col, coo_matrix.data)
    return sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)


def extract_most_relevant_keywords(feature_names, sorted_items, number_of_keywords=10):
    """
    Get the most relevant keywords.

    :param feature_names: the model feature names
    :param sorted_items: the sorted items of the model.
    :param number_of_keywords: the number of keywords to return.
    :return: the most relevant keywords
    """
    sorted_items = sorted_items[:number_of_keywords]
    score_values = []
    feature_values = []

    for index, score in sorted_items:
        score_values.append(round(score, 3))
        feature_values.append(feature_names[index])

    results = {}
    for index in range(len(feature_values)):
        results[feature_values[index]] = score_values[index]

    return results


def get_keywords(model_count_vectorizer, model_tfidf_transformer, document):
    """
    Get the keywords of a document by the model.
    """
    feature_names = model_count_vectorizer.get_feature_names()
    tf_idf_vector = model_tfidf_transformer.transform(model_count_vectorizer.transform([document]))
    sorted_items = sort_coo(tf_idf_vector.tocoo())
    keywords = extract_most_relevant_keywords(feature_names, sorted_items, NUM_OF_KEYWORDS)
    return list(keywords.keys())
