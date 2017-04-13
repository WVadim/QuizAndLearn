from constants import *
from gensim.models import word2vec
import numpy as np
import pandas as pd
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from gensim.models.keyedvectors import KeyedVectors
from nltk.tokenize import wordpunct_tokenize, word_tokenize
import re
from string import punctuation


class Preprocessor:
    def __init__(self, dataset, seed=None, include_answer=True, gather=False):
        self.model = None
        self.stemmer = SnowballStemmer('english')
        self.stopwords = [word.encode('utf-8') for word in stopwords.words('english')]
        self.dataset = pd.read_csv(dataset)
        self.include_answer = include_answer
        self.stacker = lambda x: np.vstack([np.expand_dims(i, 0) for i in x])
        self.statistics = {}
        self.gather = gather
        if seed is not None:
            self.dataset = self.dataset.sample(frac=1, random_state=seed)
        print 'Nan values :', self.dataset.isnull().sum()
        print 'Dropping it.'
        self.dataset = self.dataset.dropna()

    stop_words = ['the', 'a', 'an', 'and', 'but', 'if', 'or', 'because', 'as', 'what', 'which', 'this', 'that', 'these',
                  'those', 'then',
                  'just', 'so', 'than', 'such', 'both', 'through', 'about', 'for', 'is', 'of', 'while', 'during', 'to',
                  'What', 'Which',
                  'Is', 'If', 'While', 'This']

    def test_text_translation(self, text, remove_stop_words=True, stem_words=False):
        # Clean the text, with the option to remove stop_words and to stem words.

        # Convert words to lower case and split them
        # text = text.lower()

        # Clean the text
        text = re.sub(r"[^A-Za-z0-9]", " ", text)
        text = re.sub(r"what's", "", text)
        text = re.sub(r"What's", "", text)
        text = re.sub(r"\'s", " ", text)
        text = re.sub(r"\'ve", " have ", text)
        text = re.sub(r"can't", "cannot ", text)
        text = re.sub(r"n't", " not ", text)
        text = re.sub(r"I'm", "I am", text)
        text = re.sub(r" m ", " am ", text)
        text = re.sub(r"\'re", " are ", text)
        text = re.sub(r"\'d", " would ", text)
        text = re.sub(r"\'ll", " will ", text)
        text = re.sub(r"\0k ", "0000 ", text)
        text = re.sub(r" e g ", " eg ", text)
        text = re.sub(r" b g ", " bg ", text)
        text = re.sub(r"\0s", "0", text)
        text = re.sub(r" 9 11 ", "911", text)
        text = re.sub(r"e-mail", "email", text)
        text = re.sub(r"\s{2,}", " ", text)
        text = re.sub(r"quikly", "quickly", text)
        text = re.sub(r" usa ", " America ", text)
        text = re.sub(r" USA ", " America ", text)
        text = re.sub(r" u s ", " America ", text)
        text = re.sub(r" uk ", " England ", text)
        text = re.sub(r" UK ", " England ", text)
        text = re.sub(r"india", "India", text)
        text = re.sub(r"china", "China", text)
        text = re.sub(r"chinese", "Chinese", text)
        text = re.sub(r"imrovement", "improvement", text)
        text = re.sub(r"intially", "initially", text)
        text = re.sub(r"quora", "Quora", text)
        text = re.sub(r" dms ", "direct messages ", text)
        text = re.sub(r"demonitization", "demonetization", text)
        text = re.sub(r"actived", "active", text)
        text = re.sub(r"kms", " kilometers ", text)
        text = re.sub(r"KMs", " kilometers ", text)
        text = re.sub(r" cs ", " computer science ", text)
        text = re.sub(r" upvotes ", " up votes ", text)
        text = re.sub(r" iPhone ", " phone ", text)
        text = re.sub(r"\0rs ", " rs ", text)
        text = re.sub(r"calender", "calendar", text)
        text = re.sub(r"ios", "operating system", text)
        text = re.sub(r"gps", "GPS", text)
        text = re.sub(r"gst", "GST", text)
        text = re.sub(r"programing", "programming", text)
        text = re.sub(r"bestfriend", "best friend", text)
        text = re.sub(r"dna", "DNA", text)
        text = re.sub(r"III", "3", text)
        text = re.sub(r"the US", "America", text)
        text = re.sub(r"Astrology", "astrology", text)
        text = re.sub(r"Method", "method", text)
        text = re.sub(r"Find", "find", text)
        text = re.sub(r"banglore", "Banglore", text)
        text = re.sub(r" J K ", " JK ", text)

        # Remove punctuation from text
        text = ''.join([c for c in text if c not in punctuation])

        # Optionally, remove stop words
        if remove_stop_words:
            text = text.split()
            text = [w for w in text if not w in Preprocessor.stop_words]
            text = " ".join(text)

        # Optionally, shorten words to their stems
        if stem_words:
            text = text.split()
            stemmer = SnowballStemmer('english')
            stemmed_words = [stemmer.stem(word) for word in text]
            text = " ".join(stemmed_words)

        # Return a list of words
        return (text)

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
        if self.gather:
            old_len = len(string_list)
            new_list = [s for s in string_list if s not in self.stopwords]
            if 'STOP' not in self.statistics.keys():
                self.statistics['STOP'] = []
            self.statistics['STOP'].append(old_len - len(new_list))
            return new_list
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
        string_list = [item for item in string_list if item != u'']
        diff = max_size - len(string_list)
        result_array = string_list + [''] * max(0, diff)
        if self.gather:
            if 'ADD' not in self.statistics.keys():
                self.statistics['ADD'] = []
            if 'NEG' not in self.statistics.keys():
                self.statistics['NEG'] = []
            if 'EMP' not in self.statistics.keys():
                self.statistics['EMP'] = []
            self.statistics['ADD'].append(len(string_list))
            if diff < 0:
                self.statistics['NEG'].append(diff)
            if len(string_list) == 0:
                self.statistics['EMP'].append(1)
        return result_array[:min(max_size, len(result_array))]

    def clean_pipeline(self, string):
        string_list = self.__split_string(string)
        string_list = self.__clean_symbols(string_list)
        #string_list = self.__stopwords_removal(string_list)
        #string_list = self.__stemmer_step(string_list)
        string_list = self.__fill_until_size(string_list)
        return string_list

    def get_model_representation(self, string_list):
        numerical = None
        if self.gather:
            if 'MODEL' not in self.statistics.keys():
                self.statistics['MODEL'] = []
        null_word = self.model[self.model.index2word[0]]
        concat = lambda x, y: y if x is None else np.concatenate((x, y), axis=0)
        unknown_word = null_word
        if self.gather:
            missing = 0
            found = 0
        for item in string_list:
            try:
                vector = self.model[item]
                if self.gather:
                    found += 1
                numerical = concat(numerical, vector)
            except KeyError:
                if item == '':
                    numerical = concat(numerical, null_word)
                else:
                    if self.gather:
                        missing ++ 1
                    numerical = concat(numerical, unknown_word)
        if self.gather:
            if missing + found != 0:
                self.statistics['MODEL'].append(float(missing) / (missing + found))
            else:
                self.statistics['MODEL'].append(1.0)
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
        for i in range(0, len(self.dataset), batch_size):
            subset = self.dataset[i:min(i + batch_size, len(self.dataset))]
            yield self.dataframe_to_representation(subset)

    def reshuffle(self, seed):
        self.dataset = self.dataset.sample(frac=1, random_state=seed)