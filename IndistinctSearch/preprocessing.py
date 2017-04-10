from constants import *
from gensim.models import word2vec
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from gensim.models.keyedvectors import KeyedVectors

START_TOKEN='&&START&&'
END_TOKEN = '&&END&&'
__stemmer = SnowballStemmer('english')
__stopwords = [word.encode('utf-8') for word in stopwords.words('english')]


def __cleantxt(x):    # aangeven sentence
    x = x.lower()
    # Removing non ASCII chars
    x = x.replace(r'[^\x00-\x7f]',r' ')
    # Pad punctuation with spaces on both sides
    for char in ['.', '"', ',', '(', ')', '!', '?', ';', ':']:
        x = x.replace(char, '')
    return x

def __train_w2v(dataset, dim=W2V_DIM, save=False, load=False):
    if load:
        model = KeyedVectors.load_word2vec_format('w2v_model/w2v_model', binary=True)
        return model
    vocab = [s.split() for s in dataset]
    model = word2vec.Word2Vec(vocab, size=dim, batch_words=1, min_count=2, workers=8, null_word=1)
    if save:
        model.wv.save_word2vec_format('w2v_model/w2v_model', binary=True)
    #model.train(vocab)
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
    #return [START_TOKEN] + words + res_arr + [END_TOKEN]
    return words + res_arr

def __make_question_dataset(question, w2v_model):
    numerical = None
    appendix = []
    null_word = w2v_model.wv.index2word[w2v_model.null_word]
    for item in question:
        try:
            w2v_vector = w2v_model[item]
            if numerical is None:
                numerical = w2v_vector
            else:
                numerical = np.concatenate((numerical, w2v_vector), axis=0)
        except KeyError:
            if item == '':
                appendix.append(np.asarray(w2v_model[null_word]))
            else:
                if numerical is None:
                    numerical = w2v_model[null_word]
                else:
                    numerical = np.concatenate((numerical, w2v_model[null_word]), axis=0)
            #w2v_vector = np.asarray([0] * w2v_dim)
        #w2v_vector = w2v_vector.reshape(-1, 1)
    for item in appendix:
        if numerical is None:
            numerical = item
        else:
            numerical = np.concatenate((numerical, item), axis=0)
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
    global __stemmer, __stopwords
    words = string.split()
    words = [__stemmer.stem(word.decode('utf-8')) for word in words if word not in __stopwords]
    return ' '.join(words)

def map_dataset(dataset, log=True):
    dataset = dataset.fillna('leeg')
    if log:
        print 'Removing symbols...'
    dataset['question1'] = dataset['question1'].map(__cleantxt)
    dataset['question2'] = dataset['question2'].map(__cleantxt)
    if log:
        print 'Stemming...'
    dataset['question1'] = dataset['question1'].map(__steem_string)
    dataset['question2'] = dataset['question2'].map(__steem_string)
    return dataset

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

    datas = pd.read_csv(path)
    if sample_size is not None:
        datas = datas[0:sample_size]
    print 'Loading dataset sized :', datas.shape
    datas = map_dataset(datas, log)
    q1_list = datas['question1'].tolist()
    q2_list = datas['question2'].tolist()

    #datas_test = pd.read_csv('test.csv')
    #datas_test = map_dataset(datas_test)

    dataset = q1_list + q2_list

    if log:
        print 'Training w2v...'
    w2v_model = __train_w2v(dataset)

    if log:
        print 'Building dataset...'

    return __build_total_data(datas, w2v_model)
