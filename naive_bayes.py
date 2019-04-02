import dataset
import pandas as pd
import nltk
from sklearn.naive_bayes import GaussianNB


def naive_bayes():


def main(argv, argc):
    if argc != 2:
        print("Usage: python naive_bayes.py <training_data.txt>")
        exit(1)

    training_data_table = naive_bayes(argv)

    filter_comments(training_data_table)

def filter_comments(training_data_table):
    training_data_table['comment'] = training_data_table.comment.map(lambda x: x.lower())
    training_data_table['comment'] = training_data_table.comment.str.replace('[^\w\s]', '')

    training_data_table['comment'] = tokenize_comments(training_data_table.comment)
    training_data_table['comment'] = normalize_text(training_data_table.comment)

def tokenize_comments(comments_vector):
    return comment_vector.apply(nltk.word_tokenize)

def normalize_text(comments_vector):
    return comment_vector.apply(lambda x: [stemmer.stem(y) ])

def file_IO(argv):
    training_file = argv[1]
    training_data_table = pd.read_table(training_file,
                                        sep = '\t',
                                        header = None,
                                        names = ['tag', 'comment'])

    training_data['label'] = training_data.map({'not_ban': 0, 'ban': 1 })
    return training_data_table

if __name__ == "__main__":
    main()
