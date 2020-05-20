# Imports
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "preprocessor"))
import tensorflow as tf
import tensorflow_datasets as tfds
import json
from tf_utils import *


class DatasetPipeline(object):
    '''Represents a dataset that has been preprocessed.
    '''

    def __init__(self):

        (self.ds_train, self.ds_test), self.ds_info = self.load_dataset()

        self.preprocess()
        

    def load_dataset(self):
        '''Load the dataset from Tensorflow Datasets.
        '''

        return tfds.load('mnist',split=['train', 'test'],shuffle_files=True,as_supervised=True,with_info = True)
        

    def preprocess(self):
        '''Apply data preprocessing operations.
        '''

        self.ds_train = self.ds_train.map(map_func=normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
        self.ds_train = self.ds_train.cache()
        self.ds_train = self.ds_train.shuffle(buffer_size=self.ds_info.splits['train'].num_examples)
        self.ds_train = self.ds_train.batch(batch_size=128)
        self.ds_train = self.ds_train.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
        

    def get_training_dataset(self):
        '''Returns the training dataset.
        '''

        return self.ds_train
        

    def get_test_dataset(self):
        '''Returns the test dataset.
        '''

        return self.ds_test
        

