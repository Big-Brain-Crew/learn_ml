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

if not os.path.exists("generators/preprocessor/pipeline.py"):
    raise Exception("Must generate pipeline.py before using this script. " + \
                    "Run pipeline_generator.py to do so.")
    
from generators.preprocessor.pipeline import DatasetPipeline


def build_model():
    '''Temporary function until model code generation is made.
    '''

    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    # Compile the model
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=tf.keras.optimizers.Adam(0.001),
        metrics=['accuracy'],
    )

    return model


def train(model, ds_train, epochs):
    ''' Temporary function until model code generation is made.
    '''

    model.fit(
        ds_train,
        epochs=6)


def main(args):

    # Load the Dataset Pipeline
    ds_pipeline = DatasetPipeline()

    # Build the Model
    model = build_model()

    # Train
    train(model, ds_pipeline.get_training_dataset(), 6)

    # # Evaluate model
    # model.evaluate()

    # # Show reults
    # model.results()


if __name__ == "__main__":
    # Parse arguments
    args=None
    main(args)
