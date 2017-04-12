import pandas as pd
from gensim.models import ldamodel, word2vec
from nltk.tokenize import wordpunct_tokenize, word_tokenize
import progressbar as pb
import multiprocessing
from nltk.tag import pos_tag
from nltk.corpus import stopwords

stop = set(stopwords.words('english'))
print stop

def load_data(filename):
    print 'Loading', filename
    datas = pd.read_csv(filename)
    question_data = datas[['question1', 'question2']]
    question_data = question_data.fillna('')
    #question_data = question_data.sample(10000)
    print '...Done'
    return question_data

def tokenize_string(string):
    return wordpunct_tokenize(string)

def fill_dict(arg):
    global stop
    dataset, index = arg
    if index % 10000 == 0:
        print 'Now', index
    return [item[0] + item[1] for item in
                         pos_tag(word_tokenize(dataset[index].decode('utf-8'), 'english')) if item[1] != '.' and item[0] != '']
    #for i in range(0, len(dataset), index):
    #    dictionary[i] = [item[0] + item[1] for item in
    #                     pos_tag(word_tokenize(dataset[i].decode('utf-8'), 'english'))
    #                     if item[1] != '.' and item[0] != u'']
    #return

def find_nnp(dataset, workers=6):
    questions = dataset['question1'].tolist() + dataset['question2'].tolist()
    #dictionary = [u''] * len(questions)
    p = multiprocessing.Pool(workers)
    dictionary = p.map(fill_dict, [(questions, index) for index in range(len(questions))])
    #return output
    return dictionary

def translate_to_dictionary(dataset, tokenizer_func):
    questions = dataset['question1'].tolist() + dataset['question2'].tolist()
    dictionary = [''] * len(questions)
    print 'Tokenizing dictionary...'
    bar = pb.ProgressBar()
    for i in bar(range(len(questions))):
        try:
            dictionary[i] = tokenizer_func(questions[i].decode('utf-8'))
        except TypeError:
            print questions[i]
            exit(0)
    return dictionary

def train_w2v_model(w2v_model, dict):
    if w2v_model is None:
        w2v_model = word2vec.Word2Vec(dict, size=500, batch_words=1, min_count=1, workers=6, null_word=1, window=10)
    else:
        w2v_model.train(dict)
    return w2v_model

dataset_train = load_data('train.csv')
dataset_test = load_data('test.csv')
total_dataset = pd.concat([dataset_train, dataset_test])
print total_dataset.head()
print total_dataset.shape

dictionary = find_nnp(total_dataset)#, word_tokenize)

log = True
if log:
    import logging
    import os
    import sys

    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)

model = train_w2v_model(None, dictionary)

model.save('tt_model')