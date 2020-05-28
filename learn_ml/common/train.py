''' This script will train any predefined dataset pipeline and machine learning model.

    The dataset is formatted as a DatasetPipeline object that is generated based off a
    preprocessor config file created from UI configurations. The model will also be 
    pre-generated, but for now is defined in this file.
'''

import os
import sys
import random

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential, optimizers
from tensorflow.keras.layers import (Conv2D, Dense, Dropout, Flatten,
                                     MaxPooling2D)

import tensorflow_datasets as tfds
import argparse


def main(args):
    from pipeline import DatasetPipeline
    from model import Model

    # Load the Dataset Pipeline
    dataset = DatasetPipeline()

    # Build the Model
    model = Model(dataset.get_training_dataset())

    # Train
    model.train()

if __name__ == "__main__":
    # Parse arguments
    args=None
    main(args)
