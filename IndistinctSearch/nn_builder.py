import tensorflow as tf
from constants import *
import math


class NeuralNetwork:
    def __init__(self, ngrams, medium=W2V_DIM, relu=False, tanh=False, seed=None):
        self.ngrams = ngrams
        self.medium = medium
        self.relu = relu
        self.tanh = tanh
        if seed is not None:
            tf.set_random_seed(seed)

    @staticmethod
    def __weight_variable(shape):
        if len(shape) == 4:
            in_out = shape[0] * shape[1] + shape[3]
        else:
            in_out = shape[0] + shape[1]
        in_out = math.sqrt(6 / float(in_out))
        initial = tf.random_uniform(shape, -in_out, in_out)
        return tf.Variable(initial)

    @staticmethod
    def __bias_variable(shape):
        initial = tf.zeros(shape)  # tf.truncated_normal(shape, stddev=0.01)#tf.constant(0.01, shape=shape)
        return tf.Variable(initial)

    @staticmethod
    def __conv(x, W, strides):
        return tf.nn.conv2d(x, W, strides=strides, padding='VALID')

    @staticmethod
    def __max_pool(x, size, strides):
        return tf.nn.max_pool(x, ksize=size,
                              strides=strides, padding='VALID')

    def __add_layer(self, previous, output, n=3):
        w2v_dim = int(previous.shape[2])
        W_conv = NeuralNetwork.__weight_variable([n, w2v_dim, 1, output])
        b_conv = NeuralNetwork.__bias_variable([output])

        h_conv = NeuralNetwork.__conv(previous, W_conv, [1, 1, 1, 1]) + b_conv
        h_conv_rsh = tf.transpose(h_conv, perm=[0, 1, 3, 2])
        return h_conv_rsh

    def __build_conv_ngram(self, x, n, k):
        conv_layer = self.__add_layer(x, k, n)
        words_amount = int(conv_layer.shape[1])
        filters_amount = int(conv_layer.shape[2])
        h_pool1 = NeuralNetwork.__max_pool(conv_layer, [1, words_amount, 1, 1], [1, 1, 1, 1])
        if self.relu:
            h_pool1 = tf.nn.relu(h_pool1)
        h_pool_flat = tf.reshape(h_pool1, [-1, filters_amount])
        return h_pool_flat

    def build_convolutional_part(self, x_input, n_arr, words=AMOUNT_OF_WORDS, w2v_dim=W2V_DIM):
        x = tf.reshape(x_input, [-1, words + ADDITOR, w2v_dim, 1])
        output_layers = []
        for i in n_arr:
            new_layer = self.__build_conv_ngram(x, i, self.medium)
            output_layers.append(new_layer)
        out = tf.concat(output_layers, 1)
        return out

    def build_outter(self, q1, q2):
        convolution_result = tf.concat([q1, q2], 1)
        shape_in = int(convolution_result.shape[1])
        shape_out = shape_in
        keep_prob = tf.placeholder(tf.float32)

        if self.tanh:
            shape_out /= 2
            h_fc1_drop = tf.nn.dropout(convolution_result, keep_prob)

            W_fc1 = NeuralNetwork.__weight_variable([shape_in, shape_out])
            b_fc1 = NeuralNetwork.__bias_variable([shape_out])

            convolution_result = tf.nn.tanh(tf.matmul(h_fc1_drop, W_fc1) + b_fc1)

        h_fc2_drop = tf.nn.dropout(convolution_result, keep_prob)

        #shape = int(convolution_result.shape[1])

        W_fc2 = NeuralNetwork.__weight_variable([shape_out, 2])
        b_fc2 = NeuralNetwork.__bias_variable([2])

        result = tf.nn.softmax(tf.matmul(h_fc2_drop, W_fc2) + b_fc2)

        return result, keep_prob

    def build_network(self, question1, question2, words=AMOUNT_OF_WORDS, w2v_dim=W2V_DIM):
        q1_convolution = self.build_convolutional_part(question1, self.ngrams, words, w2v_dim)
        q2_convolution = self.build_convolutional_part(question2, self.ngrams, words, w2v_dim)
        return self.build_outter(q1_convolution, q2_convolution)