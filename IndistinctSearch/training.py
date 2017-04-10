from neural_network import build_network
from preprocessing import build_dataset
from constants import *

import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split

data = build_dataset(1000)

learning_rate = 0.1
batch_size = 100

print 'Building network...'
x_q1 = tf.placeholder(tf.float32, [None, (AMOUNT_OF_WORDS + 2) * W2V_DIM])
x_q2 = tf.placeholder(tf.float32, [None, (AMOUNT_OF_WORDS + 2) * W2V_DIM])
y = tf.placeholder(tf.float32, [None, 2])
y_conv, keep_prob = build_network(x_q1, x_q2)
split_func = lambda x: (np.transpose(np.transpose(x)[0]), np.transpose(np.transpose(x)[1]))
stack_func = lambda x: np.vstack([np.expand_dims(i, 0) for i in x])

X_all = np.transpose(np.transpose(data)[:2])
Y_all = np.transpose(np.transpose(data)[2])
Y_all = stack_func(Y_all)

print 'Training...'
cross_entropy = tf.reduce_mean(
    tf.nn.softmax_cross_entropy_with_logits(labels=y, logits=y_conv))
train_step = tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cross_entropy)
correct_prediction = tf.equal(tf.round(y_conv), y)
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


XGlobal_train, XGlobal_test, YGlobal_train, YGlobal_test = train_test_split(X_all, Y_all, train_size=0.9)
dataset_size = len(XGlobal_train)
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for i in range(0, (dataset_size/batch_size) - 1):
        x_train, y_train = XGlobal_train[batch_size * i: batch_size * (i + 1)], YGlobal_train[batch_size * i: batch_size * (i + 1)]
        split_func = lambda x: (np.transpose(np.transpose(x)[0]), np.transpose(np.transpose(x)[1]))
        x_trainq1, x_trainq2 = split_func(x_train)
        x_trainq1 = stack_func(x_trainq1)
        x_trainq2 = stack_func(x_trainq2)
        if True:
            x_testq1, x_testq2 = split_func(XGlobal_test)
            x_testq1 = stack_func(x_testq1)
            x_testq2 = stack_func(x_testq2)
            train_accuracy = accuracy.eval(feed_dict={
                x_q1: x_testq1, x_q2: x_testq2, y: YGlobal_test, keep_prob: 1})
            print('step %d, training accuracy %g' % (i, train_accuracy))
            loss_val = sess.run(cross_entropy, feed_dict={x_q1: x_testq1, x_q2: x_testq2, y: YGlobal_test, keep_prob: 1})
            print 'Loss :', loss_val
        train_step.run(feed_dict={x_q1: x_trainq1, x_q2: x_trainq2, y: y_train, keep_prob: 0.5})
    xg_q1, xg_q2 = split_func(XGlobal_test)
    xg_q1 = stack_func(xg_q1)
    xg_q2 = stack_func(xg_q2)
    print('test accuracy %g' % accuracy.eval(feed_dict={
        x_q1: xg_q1, x_q2: xg_q2, y: YGlobal_test, keep_prob: 1}))
