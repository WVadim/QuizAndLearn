import tensorflow as tf
from constants import *
import math


def __weight_variable(shape):
    if len(shape) == 4:
        in_out = shape[0] * shape[1] + shape[3]
    else:
        in_out = shape[0] + shape[1]
    in_out = math.sqrt(6/float(in_out))
    initial = tf.random_uniform(shape, -in_out, in_out)
    return tf.Variable(initial)


def __bias_variable(shape):
    initial = tf.zeros(shape)#tf.truncated_normal(shape, stddev=0.01)#tf.constant(0.01, shape=shape)
    return tf.Variable(initial)


def __conv(x, W, strides):
    return tf.nn.conv2d(x, W, strides=strides, padding='VALID')

def __max_pool(x, size, strides):
    return tf.nn.max_pool(x, ksize=size,
                        strides=strides, padding='VALID')


def add_layer(previous, output, n=3):
    w2v_dim = int(previous.shape[2])
    W_conv = __weight_variable([n, w2v_dim, 1, output])
    b_conv = __bias_variable([output])

    h_conv = __conv(previous, W_conv, [1, 1, 1, 1]) + b_conv
    h_conv_rsh = tf.transpose(h_conv, perm=[0, 1, 3, 2])
    return h_conv_rsh

def __build_conv_ngram(x, n, k):
    conv_layer = add_layer(x, k, n)
    words_amount = int(conv_layer.shape[1])
    filters_amount = int(conv_layer.shape[2])
    #print conv_layer.shape
    #print words_amount, filters_amount
    # print words_amount, filters_amount
    h_pool1 = __max_pool(conv_layer, [1, words_amount, 1, 1], [1, 1, 1, 1])
    h_pool_flat = tf.reshape(h_pool1, [-1, filters_amount])
    #print h_pool_flat.shape
    return h_pool_flat


def build_convolutional_TW(x_input, n_arr, words=AMOUNT_OF_WORDS, w2v_dim=W2V_DIM):
    x = tf.reshape(x_input, [-1, words + ADDITOR, w2v_dim, 1])
    output_layers = []
    for i in n_arr:
        new_layer = __build_conv_ngram(x, i, w2v_dim)
        output_layers.append(new_layer)
    out = tf.concat(output_layers, 1)
    #print out.shape
    return out

def build_outter(q1, q2):
    convolution_result = tf.concat([q1, q2], 1)
    shape = int(convolution_result.shape[1])

    keep_prob = tf.placeholder(tf.float32)

    h_fc1_drop = tf.nn.dropout(convolution_result, keep_prob)

    W_fc1 = __weight_variable([shape, shape])
    b_fc1 = __bias_variable([shape])

    result_tanh = tf.nn.tanh(tf.matmul(h_fc1_drop, W_fc1) + b_fc1)

    h_fc2_drop = tf.nn.dropout(result_tanh, keep_prob)

    shape = int(convolution_result.shape[1])

    W_fc2 = __weight_variable([shape, 2])
    b_fc2 = __bias_variable([2])

    result = tf.nn.softmax(tf.matmul(h_fc2_drop, W_fc2) + b_fc2)

    return result, keep_prob

def __build_convolutional_net(x, words=AMOUNT_OF_WORDS, w2d_dim = W2V_DIM):
    x_sent = tf.reshape(x, [-1, words + ADDITOR, w2d_dim, 1])
    OUTPUT_SIZE1 = w2d_dim / 2
    layers = []
    #print x_sent.shape
    h_conv1 = add_layer(x_sent, OUTPUT_SIZE1)

    OUTPUT_SIZE2 = OUTPUT_SIZE1 / 2

    h_conv2 = add_layer(h_conv1, OUTPUT_SIZE2)

    OUTPUT_SIZE3 = OUTPUT_SIZE2 / 2

    h_conv3 = add_layer(h_conv2, OUTPUT_SIZE3)
    final_conv = h_conv3
    #print final_conv.shape

    #print h_conv2.shape
    words_amount = int(final_conv.shape[1])
    filters_amount = int(final_conv.shape[2])
    #print words_amount, filters_amount

    h_pool1 = __max_pool(final_conv, [1, words_amount, 1, 1], [1, 1, 1, 1])
    print h_pool1.shape
    h_pool_flat = tf.reshape(h_pool1, [-1, filters_amount])
    #print h_pool_flat.shape
    return h_pool_flat

def __build_merged(x_f, x_s, words=AMOUNT_OF_WORDS):
    out = tf.concat([x_f, x_s], 1)
    f_shape = int(x_f.shape[1])
    s_shape = int(x_s.shape[1])
    avg_shape = f_shape + s_shape / 2
    W_fc1 = __weight_variable([f_shape + s_shape, avg_shape])
    b_fc1 = __bias_variable([avg_shape])

    h_fc1 = tf.nn.tanh(tf.matmul(out, W_fc1) + b_fc1)

    keep_prob = tf.placeholder(tf.float32)
    h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

    W_fc2 = __weight_variable([avg_shape, 2])
    b_fc2 = __bias_variable([2])

    y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)
    #y_conv = tf.reshape(y_conv, [-1])
    return y_conv, keep_prob


def build_network(question1, question2, words=AMOUNT_OF_WORDS, w2v_dim=W2V_DIM):
    q1_output = __build_convolutional_net(question1, words, w2v_dim)
    q2_output = __build_convolutional_net(question2, words, w2v_dim)
    return __build_merged(q1_output, q2_output, words)


def build_network_ZW(question1, question2, words=AMOUNT_OF_WORDS, w2v_dim=W2V_DIM):
    n_grams = range(2, 6)
    q1_convolution = build_convolutional_TW(question1, n_grams, words, w2v_dim)
    q2_convolution = build_convolutional_TW(question2, n_grams, words, w2v_dim)
    return build_outter(q1_convolution, q2_convolution)