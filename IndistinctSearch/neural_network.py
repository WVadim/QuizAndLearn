import tensorflow as tf
from constants import *


def __weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)


def __bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)


def __conv(x, W, strides):
  return tf.nn.conv2d(x, W, strides=strides, padding='VALID')


def __max_pool(x, size, strides):
  return tf.nn.max_pool(x, ksize=size,
                        strides=strides, padding='VALID')


def __build_convolutional_net(x, words=AMOUNT_OF_WORDS, w2d_dim = W2V_DIM):
    OUTPUT_SIZE1 = 1
    x_sent = tf.reshape(x, [-1, words + 2, w2d_dim, 1])
    W_conv1 = __weight_variable([3, w2d_dim, 1, OUTPUT_SIZE1 * words])
    b_conv1 = __bias_variable([OUTPUT_SIZE1 * words])

    h_conv1 = __conv(x_sent, W_conv1, [1, 1, 1, 1]) + b_conv1
    h_pool1 = __max_pool(h_conv1, [1, words, 1, 1], [1, 1, 1, 1])
    h_pool_flat = tf.reshape(h_pool1, [-1, words])

    return h_pool_flat


def __build_merged(x_f, x_s, words=AMOUNT_OF_WORDS):
    out = tf.concat([x_f, x_s], 1)
    W_fc1 = __weight_variable([words * 2, words])
    b_fc1 = __bias_variable([words])

    h_fc1 = tf.nn.sigmoid(tf.matmul(out, W_fc1) + b_fc1)

    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    W_fc2 = __weight_variable([words, 2])
    b_fc2 = __bias_variable([2])

    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
    #y_conv = tf.reshape(y_conv, [-1])
    return y_conv, keep_prob

def build_network(question1, question2, words=AMOUNT_OF_WORDS, w2v_dim=W2V_DIM):
    q1_output = __build_convolutional_net(question1, words, w2v_dim)
    q2_output = __build_convolutional_net(question2, words, w2v_dim)
    return __build_merged(q1_output, q2_output, words)

