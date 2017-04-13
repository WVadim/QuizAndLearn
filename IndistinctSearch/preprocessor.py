from constants import *
from gensim.models import word2vec
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from gensim.models.keyedvectors import KeyedVectors
from nltk.tokenize import wordpunct_tokenize, word_tokenize


class Preprocessor:
    def __init__(self, dataset, seed=None, include_answer=True):
        self.model = None
        self.stemmer = SnowballStemmer('english')
        self.stopwords = [word.encode('utf-8') for word in stopwords.words('english')]
        self.dataset = pd.read_csv(dataset)
        self.include_answer = include_answer
        self.stacker = lambda x: np.vstack([np.expand_dims(i, 0) for i in x])
        if seed is not None:
            self.dataset = self.dataset.sample(frac=1, random_state=seed)
        print 'Nan values :', self.dataset.isnull().sum()
        print 'Dropping it.'
        self.dataset = self.dataset.dropna()

    def size(self):
        return len(self.dataset)

    def load_model(self, model_name, binary=True):
        self.model = KeyedVectors.load_word2vec_format(model_name, binary=binary)

    def create_model(self, corpus, size, batch, min_count, workers, null_word):
        model = word2vec.Word2Vec(corpus, size=size, batch_words=batch,
                                  min_count=min_count, workers=workers, null_word=null_word)
        self.model = model.wv

    def __stemmer_step(self, string_list):
        return [self.stemmer.stem(s) for s in string_list]

    def __stopwords_removal(self, string_list):
        return [s for s in string_list if s not in self.stopwords]

    def __clean_symbols_string(self, string, symbols):
        for s in symbols:
            string = string.replace(s, '')
        return string

    def __clean_symbols(self, string_list):
        list_of_symbols = ['.', '"', ',', '(', ')', '!', '?', ';', ':']
        return [self.__clean_symbols_string(s, list_of_symbols) for s in string_list]

    def __split_string(self, string):
        return wordpunct_tokenize(string.decode('utf-8'))

    def __fill_until_size(self, string_list, max_size=AMOUNT_OF_WORDS):
        diff = max_size - len(string_list)
        result_array = string_list + [''] * max(0, diff)
        return result_array[:min(max_size, len(result_array))]

    def clean_pipeline(self, string):
        string_list = self.__split_string(string)
        string_list = self.__clean_symbols(string_list)
        string_list = self.__stopwords_removal(string_list)
        string_list = self.__stemmer_step(string_list)
        string_list = self.__fill_until_size(string_list)
        return string_list

    def get_model_representation(self, string_list):
        numerical = None
        null_word = self.model[self.model.index2word[0]]
        concat = lambda x, y: y if x is None else np.concatenate((x, y), axis=0)
        unknown_word = null_word
        for item in string_list:
            try:
                vector = self.model[item]
                numerical = concat(numerical, vector)
            except KeyError:
                if item == '':
                    numerical = concat(numerical, null_word)
                else:
                    numerical = concat(numerical, unknown_word)
        return numerical

    def get_row_representation(self, row):
        question1 = row['question1']
        question2 = row['question2']
        question1 = self.clean_pipeline(question1)
        question2 = self.clean_pipeline(question2)

        duplicate_val = [0, 0]
        if self.include_answer:
            duplicate_val[row['is_duplicate']] = 1

        duplicate_val = np.asarray(duplicate_val)
        return self.get_model_representation(question1), \
               self.get_model_representation(question2), duplicate_val

    def dataframe_to_representation(self, dataframe):
        x1_result = []
        x2_result = []
        y_result = []
        for index, row in dataframe.iterrows():
            x1, x2, y = self.get_row_representation(row)
            x1_result.append(x1)
            x2_result.append(x2)
            y_result.append(y)
        x1_result = np.asarray(x1_result)
        x2_result = np.asarray(x2_result)
        y_result = self.stacker(y_result)
        return x1_result, x2_result, y_result

    def make_testset(self, size):
        return self.dataframe_to_representation(self.dataset.sample(size))

    def iterate_batches(self, batch_size):
        for i in range(batch_size, len(self.dataset), batch_size):
            subset = self.dataset[i - batch_size:i]
            yield self.dataframe_to_representation(subset)

    def reshuffle(self, seed):
        self.dataset = self.dataset.sample(frac=1, random_state=seed)