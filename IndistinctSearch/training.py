from neural_network import build_network, build_network_ZW
from preprocessing import build_dataset
from constants import *

import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split, ShuffleSplit
import csv
import random


learning_rate = 0.00005
batch_size = 50
save = False

def transfer_to_doublearr(arr):
    x_trainq1, x_trainq2 = split_func(arr)
    x_trainq1 = stack_func(x_trainq1)
    x_trainq2 = stack_func(x_trainq2)
    return x_trainq1, x_trainq2

def split_data(X, Y, train_size):
    x_train, x_test, y_train, y_test = train_test_split(X, Y, train_size=train_size)
    x_trainq1, x_trainq2 = transfer_to_doublearr(x_train)
    x_testq1, x_testq2 = transfer_to_doublearr(x_test)
    return x_trainq1, x_trainq2, y_train, x_testq1, x_testq2, y_test


print 'Building network...'
x_q1 = tf.placeholder(tf.float32, [None, (AMOUNT_OF_WORDS + ADDITOR) * W2V_DIM])
x_q2 = tf.placeholder(tf.float32, [None, (AMOUNT_OF_WORDS + ADDITOR) * W2V_DIM])
y = tf.placeholder(tf.float32, [None, 2])
y_conv, keep_prob = build_network_ZW(x_q1, x_q2)
split_func = lambda x: (np.transpose(np.transpose(x)[0]), np.transpose(np.transpose(x)[1]))
stack_func = lambda x: np.vstack([np.expand_dims(i, 0) for i in x])
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_conv))
train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy)
#correct_prediction = tf.equal(tf.round(y_conv), y)
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


index = 0
bsize = 10000

sess = tf.Session()
sess.run(tf.global_variables_initializer())

while True:

    data, total_size = build_dataset(sample_high=(index + 1) * bsize, sample_low=index * bsize)
    index += 1
    if len(data) == 0:
        break
    X_all = np.transpose(np.transpose(data)[:2])
    Y_all = np.transpose(np.transpose(data)[2])
    Y_all = stack_func(Y_all)

    print 'Training...'

    if save:
        saver = tf.train.Saver()

    dataset_size = len(X_all)
    lcounter = 0
    shuffle_counter = 0
    try:
        for order in range(1):
            shuffle_counter = 0
            split = ShuffleSplit(n_splits=3, test_size=0.1)
            for train_index, test_index in split.split(X_all):
                shuffle_counter += 1
                x_train_q1, x_train_q2 = transfer_to_doublearr(X_all[train_index])
                y_train = Y_all[train_index]
                x_test_q1, x_test_q2 = transfer_to_doublearr(X_all[test_index])
                y_test = Y_all[test_index]
                dataset_size = len(x_train_q1)
                lcounter = 0
                for i in range(0, dataset_size - batch_size, batch_size):
                    batch_xq1_train = x_train_q1[i: i + batch_size]
                    batch_xq2_train = x_train_q2[i: i + batch_size]
                    batch_y_train = y_train[i: i + batch_size]
                    if random.randint(0, 1000) % 2 == 0:
                        sess.run(train_step,
                             feed_dict={x_q1: batch_xq1_train, x_q2: batch_xq2_train, y: batch_y_train, keep_prob: 1})
                    else:
                        sess.run(train_step,
                             feed_dict={x_q1: batch_xq2_train, x_q2: batch_xq1_train, y: batch_y_train, keep_prob: 1})
                    if lcounter % 20 == 0:
                        train_accuracy = sess.run(accuracy, feed_dict={x_q1: x_test_q1, x_q2: x_test_q2, y: y_test, keep_prob: 1})
                        loss_val = sess.run(cross_entropy, feed_dict={x_q1: x_test_q1, x_q2: x_test_q2, y: y_test, keep_prob: 1})
                        print('data gathered %d out of %d, order %d, shuffle %d, step %d out of %d, training accuracy %g, training loss %g' %
                              (index * bsize, total_size, order, shuffle_counter, i, dataset_size, train_accuracy, loss_val))
                    lcounter += 1
        if save:
            saver.save(sess, 'nn_conv_TW_model')
        del data
        del X_all, Y_all
    except KeyboardInterrupt:
        break

counter = 0
index = 0
bsize = 5000
output_file = open('submission.csv', 'w')
output_file.close()
while True:
    print 'Predictiong next', index, 'batch...'
    data_evaluate, total_size = build_dataset(sample_high=(index + 1) * bsize, sample_low=index * bsize, path='test.csv', no_answer=True)
    if len(data_evaluate) == 0:
        break
    X_evaluate = np.transpose(np.transpose(data_evaluate)[:2])
    Y_evaluate = np.transpose(np.transpose(data_evaluate)[2])
    XE_q1, XE_q2 = transfer_to_doublearr(X_evaluate)
    Y_evaluate = stack_func(Y_evaluate)
    predictions = sess.run(y_conv, feed_dict={x_q1: XE_q1, x_q2: XE_q2, y: Y_evaluate, keep_prob: 1})
    print 'Done, writing to file...'
    with open('submission.csv', 'a') as f:
        writer = csv.writer(f)
        for item in predictions:
            row = [counter, item[1]]
            writer.writerow(row)
            counter += 1
    print 'Done, going to next file...'
    index += 1
