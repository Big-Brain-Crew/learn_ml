''' 
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
import subprocess
import json


def results(results_dir="./project/results"):
    if results_dir.endswith("/"):
        results_dir = results_dir[:-1]

    # Load model folders
    models = os.listdir(results_dir)

    # Load all results data from the dicts
    results = {}
    for model in models:
        results[model] = json.load(open("{dir}/{model}/results.json".format(dir=results_dir,model=model)))

    # Print them as a table
    print("================================ RESULTS ================================")
    for model, result in results.items():
        print("{model} - loss: {loss}, accuracy: {accuracy}".format(model=model, loss=result['loss'], accuracy=result['accuracy']))
    


def main():
    results()


if __name__ == "__main__":
    main()
