import sys
import pickle

from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score

class Classifier:

    def __init__(self, ban_bias=0.5, test_size=0.2):
        """
        Initialize a Classifier

        :param ban_bias: Percentage of training data that should be bans.
        :param test_size: Percentage of training data that should used when testing.
        """
        self.classifier = Pipeline([("vect", CountVectorizer(encoding="utf-8", decode_error="replace")),
                                    ("tfidf", TfidfTransformer()),
                                    ("clf", MultinomialNB())])
        self.ban_bias = ban_bias
        self.test_size = test_size

        self.score = None
        self.ban_accuracy = None
        self.non_ban_accuracy = None

    def train(self, dataset):
        df = pd.read_csv(dataset, encoding="utf-8")
        df["text"] = df["text"].fillna("")

        text_column = df.columns.get_loc("text")
        ban_column = df.columns.get_loc("ban")

        # create datset using ALL bans and where (1 - ban_bias) datapoints are not bans
        bans = df.loc[df["ban"] == 1]
        non_bans = df.loc[df["ban"] == 0]
        if self.ban_bias:
            non_bans = non_bans.sample(int(len(bans) * (1 / self.ban_bias - 1)))
        data = pd.concat([bans, non_bans])

        # split dataset into training and testing components of test_size and (1 - test_size)
        train, test = train_test_split(data.to_numpy(), test_size=self.test_size)

        train_X = [point[text_column] for point in train]
        train_y = [point[ban_column] for point in train]
        self.classifier.fit(train_X, train_y)

        test_X = [point[text_column] for point in test]
        test_y = [point[ban_column] for point in test]
        y_pred = self.classifier.predict(test_X)
        matrix = confusion_matrix(test_y, y_pred)
        true_negative, false_positive, false_negative, true_positive = matrix.ravel()

        self.score = accuracy_score(test_y, y_pred)
        self.ban_accuracy = true_positive / (true_positive + false_negative)
        self.non_ban_accuracy = true_negative / (true_negative + false_positive)
        return self.score

    def predict(self, data):
        return [bool(prediction) for prediction in self.classifier.predict(data)]

    def save(self, path):
        Path(path).write_bytes(pickle.dumps(self.__dict__))

    @classmethod
    def load(cls, path):
        clf = cls()
        clf.__dict__.update(pickle.loads(Path(path).read_bytes()))
        return clf

if __name__ == "__main__":
    clf = Classifier()
    clf.train("datasets/dataset.csv")
    clf.save("models/my_classifier.pkl")

    print("score", clf.score)
    print("ban_accuracy", clf.ban_accuracy)
    print("non_ban_accuracy", clf.non_ban_accuracy)
