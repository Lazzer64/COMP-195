import sys
import pickle

from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline

class Classifier:

    def __init__(self):
        self.classifier = Pipeline([("vect", CountVectorizer(encoding="utf-8", decode_error="replace")),
                                    ("tfidf", TfidfTransformer()),
                                    ("clf", MultinomialNB())])
        self.score = None

    def train(self, dataset):
        df = pd.read_csv(dataset, encoding="utf-8")
        df["text"] = df["text"].fillna("")

        text_column = df.columns.get_loc("text")
        ban_column = df.columns.get_loc("ban")

        # select all bans and an equal number of non-bans
        bans = df.loc[df["ban"] == 1]
        other = df.loc[df["ban"] == 0]
        data = pd.concat([bans, other])
        print(f"Using {len(data)} data points.")

        train, test = train_test_split(data.to_numpy(), test_size=0.2)

        train_X = [point[text_column] for point in train]
        train_y = [point[ban_column] for point in train]
        self.classifier.fit(train_X, train_y)

        test_X = [point[text_column] for point in test]
        test_y = [point[ban_column] for point in test]
        self.score = self.classifier.score(test_X, test_y)
        return self.score

    def predict(self, data):
        return [bool(prediction) for prediction in self.classifier.predict(data)]

    def save(self, path):
        Path(path).write_bytes(pickle.dumps(self))

    @classmethod
    def load(cls, path):
        return pickle.loads(Path(path).read_bytes())

if __name__ == "__main__":
    clf = Classifier()
    print(clf.train("datasets/dataset.csv"))
