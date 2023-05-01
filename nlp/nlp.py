import pandas as pd
from datetime import datetime
from sentence_transformers import SentenceTransformer
import umap
import hdbscan
from nlp.utils import (
    process_time,
    preprocess_text,
    c_tf_idf,
    extract_top_n_words_per_topic,
)


class NLP:
    def __init__(self) -> None:
        # Load the reviews
        self.reviews_df = pd.read_csv("data/processed_reviews.csv")

        # Preprocess time
        self.reviews_df["date"] = self.reviews_df.time_ago.map(process_time)
        self.reviews_df["date"] = pd.to_datetime(self.reviews_df["date"])

        # Preprocess and clean the text
        self.preprocess_text()

    def preprocess_text(self) -> None:
        self.documents = self.reviews_df.copy()

        self.documents = self.documents.loc[
            self.reviews_df.lang == "fr", ["text", "stars", "date"]
        ]

        self.documents["processed_text"] = preprocess_text(self.documents.text)

        # Dropping duplicates and empty strings
        self.documents = self.documents.drop_duplicates(subset="processed_text")
        self.documents = self.documents.drop(
            index=self.documents[self.documents.processed_text.str.len() == 0].index
        )

        # droping an outlier review that screws the clustering
        self.documents = self.documents.drop(index=191)

    def get_reviews(self, start: datetime, end: datetime):
        return (
            self.reviews_df.loc[
                (self.reviews_df.date >= start) & (self.reviews_df.date <= end),
                ["text", "stars", "date"],
            ]
            .fillna("")
            .to_dict("records")
        )

    def get_strength_weaknesses(self, start: datetime, end: datetime) -> dict:
        docs_df = self.documents.copy()

        # filter for reviews between start and end
        docs_df = docs_df[(docs_df.date >= start) & (docs_df.date <= end)]

        # filtering out neutral reviews
        docs_df = docs_df[docs_df.stars != 3]

        # cluster is 0 if rating <=2 and 1 if rating >=4
        docs_df["cluster"] = 0
        docs_df.loc[docs_df.stars >= 4, "cluster"] = 1

        docs_by_cluster = docs_df.groupby("cluster", as_index=False).agg(
            {"processed_text": " ".join}
        )

        tf_idf, count = c_tf_idf(
            docs_by_cluster.processed_text.values,
            m=len(docs_df.processed_text),
            ngram_range=(3, 3),
        )

        return extract_top_n_words_per_topic(tf_idf, count, docs_by_cluster)

    def get_clusters(self, start: datetime, end: datetime):
        docs_df = self.documents.copy()

        # filter for reviews between start and end
        docs_df = docs_df[(docs_df.date >= start) & (docs_df.date <= end)]

        # make the embeddings
        model = SentenceTransformer("distiluse-base-multilingual-cased-v1")
        embeddings = model.encode(docs_df.processed_text.to_list())

        # reduce dimensions
        reducer = umap.UMAP(
            n_neighbors=15,
            n_components=10,
            metric="cosine",
            random_state=42,
        ).fit(embeddings)
        reduced = reducer.transform(embeddings)

        # make clusters
        clusterer = hdbscan.HDBSCAN(min_cluster_size=20, min_samples=5).fit(reduced)
        docs_df["cluster"] = clusterer.labels_

        # compute topics for clusters
        docs_by_cluster = docs_df.groupby("cluster", as_index=False).agg(
            {"processed_text": " ".join}
        )
        tf_idf, count = c_tf_idf(
            docs_by_cluster.processed_text.values,
            m=len(docs_df.processed_text),
            ngram_range=(3, 3),
        )

        # compute the x,y coordinates of the reviews
        reducer_plotting = umap.UMAP(
            n_neighbors=15, n_components=2, metric="cosine", random_state=42
        ).fit(embeddings)
        doc_coord = reducer_plotting.transform(embeddings)
        docs_df["x"] = doc_coord[:, 0]
        docs_df["y"] = doc_coord[:, 1]

        return {
            "clusters": extract_top_n_words_per_topic(tf_idf, count, docs_by_cluster),
            "reviews": docs_df[["text", "cluster", "x", "y"]].to_dict("records"),
        }
