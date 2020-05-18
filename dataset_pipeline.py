### ------------------------------------------------------------------------------------ ###
#
#  Contains DatasetPipeline classes that define all data formatting
#  and preprocessing required before model training. This may involve to
#  include automatic pipeline generation, but for now will be based off
#  datasets available from Tensorflow datasets (https://www.tensorflow.org/datasets)
#
### ------------------------------------------------------------------------------------ ###

import tensorflow as tf
import tensorflow_datasets as tfds
import json


# Load Tensorflow Datasets and preprecess them.
class DatasetPipeline(object):
    def __init__(self, dataset='mnist'):

        (self.ds_train, self.ds_test), self.ds_info = self.load_dataset(dataset)

        self.preprocess()

    # Load the dataset from Tensorflow Datasets URL
    def load_dataset(self, dataset):

        # This will be filled out by the JSON

        # Example
        return tfds.load('mnist',
                         split=[
                             'train', 'test'],
                         shuffle_files=True,
                         as_supervised=True,
                         with_info=True)

    # Preprocess the dataset based of JSON config file
    def preprocess(self):

        # This will be filled out by the JSON

        # Example
        self.ds_train = ds_train.batch(128)
