import sys
import glob
import pdb
import pandas as pd
import numpy as np
import nltk
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix

def main(argv, argc):
    if argc != 2:
        print("Usage: python naive_bayes.py <training_data.txt>")
        exit(1)

    training_data_table = file_IO(argv)

    training_data_table, counts = filter_comments(training_data_table)
    x_test, y_test, naive_bayes_model = fit_data(training_data_table, counts)
    output_prediction = test_model_accuracy(naive_bayes_model, x_test)
    print(np.mean(output_prediction == y_test))

    print(confusion_matrix(y_test, output_prediction))
    pdb.set_trace()


def filter_comments(training_data_table):
    training_data_table['comment'] = training_data_table['comment'].map(lambda x: x.lower())
    training_data_table['comment'] = training_data_table['comment'].str.replace('[^\w\s]', '')

#   tokenize the data
    training_data_table['comment'] = tokenize_comments(training_data_table['comment'])
#   normalize the data
    training_data_table['comment'] = normalize_text(training_data_table['comment'])
#   transform the data into occurences
    training_data_table['comment'], counts = extrapolate_into_occurences(training_data_table['comment'])

    return training_data_table, counts


def fit_data(training_data_table, counts):
    x_train, x_test, y_train, y_test = split_data(training_data_table['tag'], counts)
    return x_test, y_test, MultinomialNB().fit(x_train, y_train)

def test_model_accuracy(naive_bayes_model, x_test):
    return naive_bayes_model.predict(x_test)


def split_data(tag_vector, counts):
    return train_test_split(counts, tag_vector, train_size = 0.8)

def tokenize_comments(comments_vector):
    return comments_vector.apply(nltk.word_tokenize)

def normalize_text(comments_vector):
    norm = PorterStemmer()
    return comments_vector.apply(lambda x: [norm.stem(y) for y in x])

def extrapolate_into_occurences(comments_vector):
    comments_vector = comments_vector.apply(lambda x: ' '.join(x))
#   apply tf-idf
    counts = CountVectorizer().fit_transform(comments_vector)
    return comments_vector, counts

def file_IO(argv):
    '''
#   reads from a text file
#   python main.py dataset.txt

    training_file = argv[1]

    training_data_table = pd.read_table(training_file,
                                        sep = '\t',
                                        header = None,
                                        names = ['tag', 'comment'])

    training_data['label'] = training_data.map({'not_ban': 0, 'ban': 1 })

    '''

#   reads from the naive_bayes_files directory
#   python main.py naive_bayes_files/Hamilton naive_bayes_files/Madison

    data_set = {'tag': [], 'comment': []}
    directory_files = []
    for i in range(1, len(argv)):
        directory_files.append(glob.glob(argv[i]+"/*.txt"))
        for j in range(len(directory_files[i-1])):
            data_set['tag'].append(argv[i])

    for files in directory_files:
        for file in files:
            text = file_data_to_string(open(file, "r"))
            data_set['comment'].append(text)

    training_data_table = pd.DataFrame(data_set, columns = ['tag', 'comment'])

    return training_data_table


def file_data_to_string(file):
    result = ""
    for l in file.readlines():
        result += l
    return result

if __name__ == "__main__":
    main(sys.argv, len(sys.argv))
