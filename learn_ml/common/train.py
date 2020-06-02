''' This script will train any predefined dataset pipeline and machine learning model.

    The dataset is formatted as a DatasetPipeline object that is generated based off a
    preprocessor config file created from UI configurations. The model will also be
    pre-generated, but for now is defined in this file.
'''

import os
import sys

import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import Sequential, optimizers
from tensorflow.keras.layers import (Conv2D, Dense, Dropout, Flatten,
                                     MaxPooling2D)

import tensorflow_datasets as tfds
import argparse
import subprocess


def create_assets(pipeline_file, model_file):

    subprocess.Popen(["cp", "project/pipelines/{pipeline}".format(
        pipeline=pipeline_file + ".py"), "project/assets/pipeline.py"])

    subprocess.Popen(["cp", "project/models/{model}".format(
        model=model_file + ".py"), "project/assets/model.py"])


def train(pipeline_name, model_name):
    create_assets(pipeline_name, model_name)

    from assets.pipeline import DatasetPipeline
    from assets.model import Model

    # Load the Dataset Pipeline
    dataset = DatasetPipeline()

    # Build the Model
    model = Model(dataset)

    # Train
    model.train()

    # Evaluate the model
    model.evaluate()

    # Save the model
    model.save("./project/results/" + model_name)


def main(args):

    train(args.pipeline, args.model)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--pipeline", help="name of the pipeline file.")
    parser.add_argument("-m", "--model", help="name of the model file")
    args = parser.parse_args()
    main(args)
