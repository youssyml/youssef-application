import re
from datetime import datetime, timedelta

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
import spacy

TIME_OF_SCRAPPING = datetime(year=2023, month=4, day=26, hour=15, minute=50)


def process_time(time_ago: str) -> datetime:
    """
    Processed the time ago field and converts it to a datetime
    by substrating the right amount of time to the date of scrapping.
    Args
        time_ago: a string with how long ago the review was left (e.g 10 months ago)
    Returns
        the datetime at which the review was left
    """

    period = re.sub("\d+", "", time_ago.strip("il y a"))
    digits = re.findall("\d+", time_ago)
    delta = int(digits[0]) if digits else 1
    if "an" in period:
        return TIME_OF_SCRAPPING - timedelta(days=delta * 365.25)
    if "mois" in period:
        return TIME_OF_SCRAPPING - timedelta(days=delta * 30.5)

    if "semaine" in period:
        return TIME_OF_SCRAPPING - timedelta(weeks=delta)

    if "jour" in period:
        return TIME_OF_SCRAPPING - timedelta(days=delta)

    if "heure" in period:
        return TIME_OF_SCRAPPING - timedelta(hours=delta)


PUNCTUATION = '!"#$%&()*+,-./:;<=>?@[\]^_`{|}~'


def preprocess_text(txt: pd.Series) -> pd.Series:
    """
    Takes the pd.Series containing the raw text and preprocesses it.
    It strips the text of digits and symbols, lowercases it.
    It also removes stop words and performs lemmatization.
    Args
        the pd.Series containing the raw text
    Returns
        a pd.Series containing processed text
    """
    # strip and lower and remove digits and punctuation
    nlp = spacy.load("fr_core_news_sm")
    processed_txt = txt.str.strip().str.lower()
    processed_txt = processed_txt.map(
        lambda doc: "".join(
            [c for c in doc if not c.isdigit() and not c in PUNCTUATION]
        )
    )

    # lemmatize and remove stop words
    processed_txt = processed_txt.map(
        lambda doc: " ".join([token.lemma_ for token in nlp(doc) if not token.is_stop])
    )
    return processed_txt


def c_tf_idf(
    documents_by_cluster: np.ndarray,
    m: int,
    ngram_range: tuple = (1, 1),
    min_df: float = 0.05,
    max_df: float = 0.95,
) -> np.ndarray:
    """
    Computes c_tf_idf for all ngrams in the documents
    Args
        documents: the numpy array containing processed documents aggregated by cluster
        m: the total number of documents before aggregation
        ngram_range: the ngram range for the vectorization
        min_df: the minimum document frequency for terms
        max_df: the maximum document frequency for terms
    Returns
        a np.array with all c_tf_idf scores for each ngram
    """
    vectorizer = CountVectorizer(
        ngram_range=ngram_range, min_df=min_df, max_df=max_df
    ).fit(documents_by_cluster)
    X = vectorizer.transform(documents_by_cluster).toarray()
    c_tf = np.divide(X.T, np.sum(X, axis=1))
    idf = np.log(np.divide(m, np.sum(X, axis=0))).reshape(-1, 1)
    return np.multiply(c_tf, idf), vectorizer


def extract_top_n_words_per_topic(
    tf_idf: np.ndarray, count: CountVectorizer, docs_by_cluster: np.ndarray, n: int = 3
) -> dict:
    """
    Compute the top n ngrams for each cluster
    Args
        tf_idf: all c_tf_idf scores of the ngrams
        count: the CountVectorize objects to get the ngram words
        docs_by_cluster: the aggregated documents by cluster
        n: the desired number of ngrams to return
    Returns
        A dictionnary with the list of top ngrams for each cluster
    """
    words = pd.DataFrame(
        tf_idf,
        index=count.get_feature_names_out(),
        columns=docs_by_cluster.cluster.values,
    )
    top_words = {k: words[k].sort_values(ascending=False)[:n] for k in words.columns}
    return top_words
