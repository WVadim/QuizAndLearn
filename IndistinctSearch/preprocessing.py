from constants import *
from gensim.models import word2vec
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from gensim.models.keyedvectors import KeyedVectors
from nltk.tokenize import wordpunct_tokenize, word_tokenize
import progressbar as pb
from nltk.tag import pos_tag


START_TOKEN='&&START&&'
END_TOKEN = '&&END&&'
__stemmer = SnowballStemmer('english')
__stopwords = [word.encode('utf-8') for word in stopwords.words('english')]


def __cleantxt(x):    # aangeven sentence
    #x = x.lower()
    # Removing non ASCII chars
    #x = x.replace(r'[^\x00-\x7f]',r' ')
    # Pad punctuation with spaces on both sides
    for char in ['.', '"', ',', '(', ')', '!', '?', ';', ':']:
        x = x.replace(char, ' ' + char + ' ')
    return x#.encode('utf-8')

def __train_w2v(dataset, dim=W2V_DIM, save=False, load=False, w2v_model=None):
    if load:
        if w2v_model is not None:
            return w2v_model
        else:
            model = word2vec.Word2Vec.load('en_1000_no_stem/en.model')
            return model
            #model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
            #return model
    else:
        vocab = [wordpunct_tokenize(s) for s in dataset]
        if w2v_model is None:
            model = word2vec.Word2Vec(vocab, size=dim, batch_words=1, min_count=2, workers=8, null_word=1)
            #model = model.wv
        else:
            return w2v_model
        if save:
            model.wv.save_word2vec_format('w2v_model/w2v_model', binary=True)
    return model


def __wrap_question(row, qname, words_size=AMOUNT_OF_WORDS):
    q = row[qname]
    words = wordpunct_tokenize(q)
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
    null_word = w2v_model[w2v_model.wv.index2word[w2v_model.null_word]]
    unknown_word = null_word#np.random.normal(0, 0.01, len(null_word))
    for item in question:
        try:
            w2v_vector = w2v_model[item]
            if numerical is None:
                numerical = w2v_vector
            else:
                numerical = np.concatenate((numerical, w2v_vector), axis=0)
        except KeyError:
            if item == '':
                appendix.append(null_word)
            else:
                if numerical is None:
                    numerical = unknown_word
                else:
                    numerical = np.concatenate((numerical, unknown_word), axis=0)
    for item in appendix:
        if numerical is None:
            numerical = item
        else:
            numerical = np.concatenate((numerical, item), axis=0)
    return numerical


def __build_data_row(row, w2v_model, no_answer):
    q1_dataset = get_nnp_repr(row['question1'].tolist()[0])#__wrap_question(row, 'question1')
    q2_dataset = get_nnp_repr(row['question2'].tolist()[0])#__wrap_question(row, 'question2')
    q1_num = __make_question_dataset(q1_dataset, w2v_model)
    q2_num = __make_question_dataset(q2_dataset, w2v_model)
    duplicate_val = [0, 0]
    if no_answer:
        duplicate_val[0] = 1
    else:
        duplicate_val[row['is_duplicate']] = 1
    return np.asarray([q1_num, q2_num, np.asarray(duplicate_val)])


def __build_total_data(dataset, model, no_answer):
    new_dataset = []
    for index, row in dataset.iterrows():
        new_dataset.append(__build_data_row(row, model, no_answer))
    return np.asarray(new_dataset)


def __steem_string(string):
    global __stemmer, __stopwords
    words = string.split()
    words = [__stemmer.stem(word.decode('utf-8')) for word in words]# if word not in __stopwords]
    return ' '.join(words)


def map_dataset(dataset, log=True):
    dataset = dataset.fillna('leeg')
    if log:
        print 'Removing symbols...'
    dataset['question1'] = dataset['question1'].map(__cleantxt)
    dataset['question2'] = dataset['question2'].map(__cleantxt)
    if log:
        print 'Stemming...'
    #dataset['question1'] = dataset['question1'].map(__steem_string)
    #dataset['question2'] = dataset['question2'].map(__steem_string)
    return dataset

def static_var(varname, value):
    def decorate(func):
        setattr(func, varname, value)
        return func
    return decorate

def get_nnp_repr(string):
    return [item[0] + item[1] for item in pos_tag(word_tokenize(string.decode('utf-8'), 'english')) if item[1] != '.']

def find_nnp(dataset):
    questions = dataset['question1'].tolist() + dataset['question2'].tolist()
    dictionary = [''] * len(questions)
    print 'Tokenizing dictionary...'
    bar = pb.ProgressBar()
    for i in bar(range(len(questions))):
        try:
            dictionary[i] = [item[0] + item[1] for item in
                             pos_tag(word_tokenize(questions[i].decode('utf-8'), 'english')) if item[1] != '.']
        except TypeError:
            print questions[i]
            exit(0)
    return dictionary


@static_var('w2v_model', None)
def build_dataset(sample_high, sample_low=None, path='train.csv', log=True, no_answer=False, sampling=False):
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
    total = len(datas)
    if sampling:
        datas = datas.sample(sample_high)
    else:
        if sample_low is None:
            sample_low = 0
        if sample_high is not None:
            sample_high = min(sample_high, len(datas))
            datas = datas[sample_low:sample_high]
        else:
            datas = datas[sample_low:]
    if not no_answer:
        zeroes = datas[datas['is_duplicate'] == 0]
    print 'Loading dataset sized :', datas.shape
    #datas = map_dataset(datas, log)
    #q1_list = datas['question1'].tolist()
    #q2_list = datas['question2'].tolist()

    #datas_test = pd.read_csv('test.csv')
    #datas_test = map_dataset(datas_test)
    q_dataset = datas[['question1', 'question2']]
    dataset = find_nnp(q_dataset)#q1_list + q2_list

    if log:
        print 'Training w2v...'
    load = True
    if build_dataset.w2v_model is None:
        build_dataset.w2v_model = __train_w2v(dataset, load=load, w2v_model=None)

    if log:
        print 'Building dataset...'
    return __build_total_data(datas, build_dataset.w2v_model, no_answer), total