import re
from datetime import datetime, timedelta

import pandas as pd
import numpy as np

from sklearn.feature_extraction.text import CountVectorizer
import spacy

TIME_OF_SCRAPPING = datetime(year=2023, month=4, day=26, hour=15, minute=50)


def process_time(time_ago: str) -> None:
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


def preprocess_text(txt: pd.Series):
    # strip and lower and remove digits and punctuation
    nlp = spacy.load("fr_core_news_sm")
    processed_txt = txt.str.strip().str.lower()
    processed_txt = processed_txt.map(
        lambda doc: "".join(
            [c for c in doc if not c.isdigit() and not c in PUNCTUATION]
        )
    )

    # lemmatize using spacy
    processed_txt = processed_txt.map(
        lambda doc: " ".join([token.lemma_ for token in nlp(doc) if not token.is_stop])
    )
    return processed_txt


def c_tf_idf(documents, m, ngram_range=(1, 1), min_df=0.05, max_df=0.95):
    vectorizer = CountVectorizer(
        ngram_range=ngram_range, min_df=min_df, max_df=max_df
    ).fit(documents)
    X = vectorizer.transform(documents).toarray()
    c_tf = np.divide(X.T, np.sum(X, axis=1))
    idf = np.log(np.divide(m, np.sum(X, axis=0))).reshape(-1, 1)
    return np.multiply(c_tf, idf), vectorizer


def extract_top_n_words_per_topic(tf_idf, count, docs_by_cluster, n=5):
    words = pd.DataFrame(
        tf_idf,
        index=count.get_feature_names_out(),
        columns=docs_by_cluster.cluster.values,
    )
    top_words = {k: words[k].sort_values(ascending=False)[:n] for k in words.columns}
    return top_words
