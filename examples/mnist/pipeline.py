# Imports
import tensorflow as tf
import tensorflow_datasets as tfds
import tf_utils as tf_utils
import numpy as np


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

        self.ds_train = self.ds_train.map(map_func=tf_utils.normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
        self.ds_train = self.ds_train.cache()
        self.ds_train = self.ds_train.shuffle(buffer_size=self.ds_info.splits['train'].num_examples)
        self.ds_train = self.ds_train.batch(batch_size=128)
        self.ds_train = self.ds_train.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)

        representative_input = []
        representative_batch = next(iter(self.ds_train))
        for i in range(0, len(representative_batch)):
            image = representative_batch[0][i]
            representative_input.append(image)
        np.save("representative_dataset.npy", representative_input)
        

    def get_training_dataset(self):
        '''Returns the training dataset.
        '''

        return self.ds_train
        

    def get_test_dataset(self):
        '''Returns the test dataset.
        '''

        return self.ds_test
        

