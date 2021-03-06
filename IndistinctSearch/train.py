from preprocessor import Preprocessor
from nn_builder import NeuralNetwork
from constants import *

import tensorflow as tf
import numpy as np

learning_rate = 1e-4

seed = 543
tf.set_random_seed(seed)
network_builder = NeuralNetwork(range(2, 6), seed=seed, relu=False, tanh=False)
dataset_name = 'train.csv'

gather = False
only_gather = True

preprocessor = Preprocessor(dataset_name, seed=seed, gather=gather)

x_q1 = tf.placeholder(tf.float32, [None, (AMOUNT_OF_WORDS + ADDITOR) * W2V_DIM])
x_q2 = tf.placeholder(tf.float32, [None, (AMOUNT_OF_WORDS + ADDITOR) * W2V_DIM])
y = tf.placeholder(tf.float32, [None, 2])
y_conv, keep_prob = network_builder.build_network(x_q1, x_q2)

cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_conv))

train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy)

correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

model_name = 'GoogleNews-vectors-negative300.bin'
print 'Loading', model_name
preprocessor.load_model(model_name)
print 'Done'

epochs = 100
batch_size = 50
print_freq = 1000

total_size = preprocessor.size()

sess = tf.Session()
sess.run(tf.global_variables_initializer())

for epoch in range(epochs):
    x1_test, x2_test, y_test = preprocessor.make_testset(5000)
    counter = 0
    for batch_x1, batch_x2, batch_y in preprocessor.iterate_batches(batch_size):
        counter += 1
        if (counter * batch_size) % print_freq == 0:
            feed_dict = {x_q1: x1_test, x_q2: x2_test, y: y_test, keep_prob: 1}
            if gather:
                avg_model = float(np.mean(preprocessor.statistics['MODEL']))
                avg_stop = float(np.mean(preprocessor.statistics['STOP']))
                avg_diff = float(np.mean(preprocessor.statistics['ADD']))
                avg_neg = float(np.mean(preprocessor.statistics['NEG']))
                len_neg = float(len(preprocessor.statistics['NEG'])) / (2 * counter * batch_size)
                len_emp = float(len(preprocessor.statistics['EMP'])) / (2 * counter * batch_size)
                print('Data observer : %.4f%% Model Drop : %.2f%% Stopwords found : %.5f Sentence len : %.5f Longer : %.2f%% Empty : %.2f%%' %
                  ((1 + epoch) * 100 * float(counter * batch_size)/total_size,
                   100 * avg_model, avg_stop, avg_diff, 100 * len_neg, len_emp))
                if only_gather:
                    continue
            train_accuracy = sess.run(accuracy, feed_dict=feed_dict)
            loss_val = sess.run(cross_entropy, feed_dict=feed_dict)
            print('epoch %d data observed %.2f%%, measured accuracy %g, training loss %g' %
                  (epoch, (1 + epoch) * 100 * float(counter * batch_size)/total_size, train_accuracy, loss_val))
        sess.run(train_step,
                 feed_dict={x_q1: batch_x1, x_q2: batch_x2, y: batch_y, keep_prob: 1})
    preprocessor.reshuffle(seed + epoch * 2)

import csv
test_dataset = Preprocessor('test.csv', include_answer=False)
output_file = open('submission.csv', 'w')
writer = csv.writer(output_file)
counter = 0
for batch_x1, batch_x2, batch_y in test_dataset.iterate_batches(batch_size):
    data = sess.run(y_conv, feed_dict={x_q1: batch_x1, x_q2: batch_x2, y: batch_y, keep_prob: 1})
    for item in data:
        row = [counter, item[1]]
        writer.writerow(row)
        counter += 1
    print '%d test data observed, total %d' % (counter, test_dataset.size())
