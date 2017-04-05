from PeeWeeController import *
from gensim.models import word2vec
import re
import logging
import os
import sys

def get_dataset():
    data = Question.select()
    text = [item.text for item in data]
    return text

def avg(sentence, w2v):
    data = re.sub("[^\w]", " ",  sentence.encode('utf-8')).split()
    summary = sum([w2v[word] for word in data])
    return summary / len(data)

program = os.path.basename(sys.argv[0])
logger = logging.getLogger(program)

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
logging.root.setLevel(level=logging.INFO)

dataset = get_dataset()
print len(dataset)
vocab = [re.sub("[^\w]", " ",  s.encode('utf-8')).split() for s in dataset]
model = word2vec.Word2Vec(vocab, size=len(dataset), batch_words=1, min_count=1)

#for item in dataset:
#    print item
#    print avg(item, model)

for s in vocab:
    for item in s:
        print item
        print model.most_similar(item, topn=1)

print model