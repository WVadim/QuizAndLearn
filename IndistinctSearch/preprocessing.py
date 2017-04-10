from constants import *
from gensim.models import word2vec
import numpy as np
import pandas as pd
from nltk.stem.porter import PorterStemmer

START_TOKEN='&&START&&'
END_TOKEN = '&&END&&'
__stemmer = PorterStemmer()


def __cleantxt(x):    # aangeven sentence
    x = x.lower()
    # Removing non ASCII chars
    x = x.replace(r'[^\x00-\x7f]',r' ')
    # Pad punctuation with spaces on both sides
    for char in ['.', '"', ',', '(', ')', '!', '?', ';', ':']:
        x = x.replace(char, ' ' + char + ' ')
    return x

def __train_w2v(dataset, dim=W2V_DIM):
    vocab = [s.split() for s in dataset]
    model = word2vec.Word2Vec(vocab, size=dim, batch_words=1, min_count=2, workers=8)
    return model


def __wrap_question(row, qname, words_size=AMOUNT_OF_WORDS):
    q = row[qname]
    words = q.split()
    if len(words) > words_size:
        words = words[:words_size]
    diff = words_size - len(words)
    res_arr = []
    if diff != 0:
        res_arr = [''] * diff
    return [START_TOKEN] + words + res_arr + [END_TOKEN]


def __make_question_dataset(question, w2v_model, w2v_dim=W2V_DIM):
    numerical = None
    for item in question:
        try:
            w2v_vector = w2v_model[item]
        except KeyError:
            w2v_vector = np.asarray([0] * w2v_dim)
        #w2v_vector = w2v_vector.reshape(-1, 1)
        if numerical is None:
            numerical = w2v_vector
        else:
            numerical = np.concatenate((numerical, w2v_vector), axis=0)
    return numerical


def __build_data_row(row, w2v_model):
    q1_dataset = __wrap_question(row, 'question1')
    q2_dataset = __wrap_question(row, 'question2')
    q1_num = __make_question_dataset(q1_dataset, w2v_model)
    q2_num = __make_question_dataset(q2_dataset, w2v_model)
    duplicate_val = [0, 0]
    duplicate_val[row['is_duplicate']] = 1
    return np.asarray([q1_num, q2_num, np.asarray(duplicate_val)])


def __build_total_data(dataset, model):
    new_dataset = []
    for index, row in dataset.iterrows():
        new_dataset.append(__build_data_row(row, model))
    return np.asarray(new_dataset)


def __steem_string(string):
    global __stemmer
    words = string.split()
    words = [__stemmer.stem(word) for word in words]
    return ' '.join(words)


def build_dataset(sample_size, path='train.csv', log=True):
    if log:
        import logging
        import os
        import sys

        if log:
            program = os.path.basename(sys.argv[0])
            logger = logging.getLogger(program)

            logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
            logging.root.setLevel(level=logging.INFO)

    datas = pd.read_csv(path)  #
    datas = datas[0:sample_size]
    datas = datas.fillna('leeg')

    datas['question1'] = datas['question1'].map(__cleantxt)
    datas['question2'] = datas['question2'].map(__cleantxt)
    #datas['question1'] = datas['question1'].map(__steem_string)
    #datas['question2'] = datas['question2'].map(__steem_string)
    q1_list = datas['question1'].tolist()
    q2_list = datas['question2'].tolist()

    dataset = q1_list + q2_list

    if log:
        print 'Training w2v...'
    w2v_model = __train_w2v(dataset)

    if log:
        print 'Building dataset...'

    return __build_total_data(datas, w2v_model)
