from preprocessor import Preprocessor
from nn_builder import NeuralNetwork
from constants import *

import tensorflow as tf
import numpy as np

learning_rate = 1e-4

seed = 543
tf.set_random_seed(seed)
network_builder = NeuralNetwork(range(2, 6), seed=seed)
dataset_name = 'train.csv'

preprocessor = Preprocessor(dataset_name, seed=seed)

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
print_freq = 100

total_size = preprocessor.size()

sess = tf.Session()
sess.run(tf.global_variables_initializer())

for epoch in range(epochs):
    x1_test, x2_test, y_test = preprocessor.make_testset(5000)
    counter = 0
    for batch_x1, batch_x2, batch_y in preprocessor.iterate_batches(batch_size):
        counter += 1
        if counter % print_freq == 0:
            feed_dict = {x_q1: x1_test, x_q2: x2_test, y: y_test, keep_prob: 1}
            train_accuracy = sess.run(accuracy, feed_dict=feed_dict)
            loss_val = sess.run(cross_entropy, feed_dict=feed_dict)
            print('epoch %d data observed %.2f%%, measured accuracy %g, training loss %g' %
                  (epoch, (1 + epoch) * 100 * float(counter * batch_size)/total_size, train_accuracy, loss_val))
        sess.run(train_step,
                 feed_dict={x_q1: batch_x1, x_q2: batch_x2, y: batch_y, keep_prob: 1})