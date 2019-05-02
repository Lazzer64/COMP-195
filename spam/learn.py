import sys
import pickle

from pathlib import Path
import pdb
import pandas as pd
import numpy
from numpy import array
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.feature_extraction.text import CountVectorizer

class Classifier:

    def __init__(self, ban_bias=0.3, test_size=0.3):
        """
        Initialize a Classifier

        :param ban_bias: Percentage of training data that should be bans.
        :param test_size: Percentage of training data that should used when testing.
        """
        self.multinomialClassifier = Pipeline([("vect", CountVectorizer(encoding="utf-8", decode_error="replace")),
                                    ("tfidf", TfidfTransformer()),
                                    ("clf", MultinomialNB())])
        self.logisticRegression = LogisticRegression(random_state = 0, solver = 'lbfgs', multi_class= 'multinomial')
        self.ban_bias = ban_bias
        self.test_size = test_size

        self.score = None
        self.ban_accuracy = None
        self.non_ban_accuracy = None

    def _classifyTextData(self, train, test, train_y, text_column):
        train_x = [point[text_column] for point in train]
        test_x = [point[text_column] for point in test]

        self.multinomialClassifier.fit(train_x, train_y)
        y_pred = self.predict(test_x, self.multinomialClassifier)
        return y_pred

    def _classifyGaussianData(self, train, test, train_y):
        train_x = array([point[:-2] for point in train])
        test_x = array([point[:-2] for point in test])

        self.logisticRegression.fit(train_x, train_y)
        y_pred = self.predict(test_x, self.logisticRegression)
        return y_pred

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
        train_y = [point[ban_column] for point in train]

        multinomial_pred = self._classifyTextData(train, test, train_y, text_column)
        logistic_reg_pred = self._classifyGaussianData(train, test, train_y)
        pred = self.majority_vote(multinomial_pred, logistic_reg_pred)

        test_y = [point[ban_column] for point in test]
        matrix = confusion_matrix(test_y, pred)
        true_negative, false_positive, false_negative, true_positive = matrix.ravel()

        self.score = accuracy_score(test_y, pred)
        self.ban_accuracy = true_positive / (true_positive + false_negative)
        self.non_ban_accuracy = true_negative / (true_negative + false_positive)
        return self.score

    def majority_vote(self, multinomial_pred, logistic_reg_pred):
        pred = []
        for i in range(len(multinomial_pred)):
            if multinomial_pred[i] and logistic_reg_pred[i]:
                pred.append(True)
            else:
                pred.append(False)
        return pred

    def predict(self, data, classifier):
        return [bool(prediction) for prediction in classifier.predict(data)]

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
