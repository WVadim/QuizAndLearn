from neural_network import build_network, build_network_ZW
from preprocessing import build_dataset
from constants import *

import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split


learning_rate = 0.0001
batch_size = 100
save = True

print 'Building network...'
x_q1 = tf.placeholder(tf.float32, [None, (AMOUNT_OF_WORDS + ADDITOR) * W2V_DIM])
x_q2 = tf.placeholder(tf.float32, [None, (AMOUNT_OF_WORDS + ADDITOR) * W2V_DIM])
y = tf.placeholder(tf.float32, [None, 2])
y_conv, keep_prob = build_network_ZW(x_q1, x_q2)
split_func = lambda x: (np.transpose(np.transpose(x)[0]), np.transpose(np.transpose(x)[1]))
stack_func = lambda x: np.vstack([np.expand_dims(i, 0) for i in x])

data = build_dataset(20000)

X_all = np.transpose(np.transpose(data)[:2])
Y_all = np.transpose(np.transpose(data)[2])
Y_all = stack_func(Y_all)

print 'Training...'
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_conv))
train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy)
correct_prediction = tf.equal(tf.round(y_conv), y)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))

if save:
    saver = tf.train.Saver()

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

dataset_size = len(X_all)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for _ in range(50):
        x_train_q1, x_train_q2, y_train, x_test_q1, x_test_q2, y_test = split_data(X_all, Y_all, train_size=0.5)
        dataset_size = len(x_train_q1)
        for i in range(0, (dataset_size/batch_size) - 1):
            batch_xq1_train = x_train_q1[batch_size * i: batch_size * (i + 1)]
            batch_xq2_train = x_train_q2[batch_size * i: batch_size * (i + 1)]
            batch_y_train = y_train[batch_size * i: batch_size * (i + 1)]
            batch_xq1_test = x_test_q1[batch_size * i: batch_size * (i + 1)]
            batch_xq2_test = x_test_q2[batch_size * i: batch_size * (i + 1)]
            batch_y_test = y_test[batch_size * i: batch_size * (i + 1)]
            train_step.run(feed_dict={x_q1: batch_xq1_train, x_q2: batch_xq2_train, y: batch_y_train, keep_prob: 0.8})
            if True:
                train_accuracy = accuracy.eval(feed_dict={
                    x_q1: batch_xq1_test, x_q2: batch_xq2_test, y: batch_y_test, keep_prob: 1})
                loss_val = sess.run(cross_entropy,
                                feed_dict={x_q1: batch_xq1_test, x_q2: batch_xq2_test, y: batch_y_test, keep_prob: 1})
                print('step %d, training accuracy %g, training loss %g' % (i * batch_size, train_accuracy, loss_val))
    if save:
        saver.save(sess, 'nn_conv_TW_model')