# Imports
import tensorflow as tf
from tf_utils import *


class Model(object):
    '''Represents a Tensorflow Model.
    '''

    def __init__(self):

        self.model = self.build_model()

    def build_model(self):
        '''Build the MNIST model.
        '''

        model = tf.keras.models.Sequential([
            tf.keras.layers.Flatten(input_shape=[28, 28, 1]),
            tf.keras.layers.Dense(units=128, activation="relu"),
            tf.keras.layers.Dense(units=10, activation="softmax"),
        ])
