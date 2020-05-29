### ---------------------------------------------------------- ###
#
# Trains a simple CNN to classify MNIST digits.
#
### ---------------------------------------------------------- ###
import os, random
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
import tensorflow_datasets as tfds
from tensorflow import keras 
from tensorflow.keras import Sequential, optimizers
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dropout, Dense 

def normalize_img(image, label):
    """Normalizes images: `uint8` -> `float32`."""
    return tf.cast(image, tf.float32) / 255., label
    
def main():
    
    # Load the MNIST dataset
    (ds_train, ds_test), ds_info = tfds.load('mnist',
                                            split=['train', 'test'],
                                            shuffle_files=True,
                                            as_supervised=True,
                                            with_info=True)

    # Training pipeline
    ds_train = ds_train.map(normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    ds_train = ds_train.cache()
    ds_train = ds_train.shuffle(ds_info.splits['train'].num_examples)
    ds_train = ds_train.batch(128)
    ds_train = ds_train.prefetch(tf.data.experimental.AUTOTUNE)

    representative_input = []
    representative_batch = next(iter(ds_train))
    for i in range(0, len(representative_batch)):
        image = representative_batch[0][i]
        representative_input.append(image)
    np.save("representative_dataset.npy", representative_input)
    
    # Testing pipeline
    ds_test = ds_test.map(normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    ds_test = ds_test.batch(128)
    ds_test = ds_test.cache()
    ds_test = ds_test.prefetch(tf.data.experimental.AUTOTUNE)

    # Build model
    model = tf.keras.models.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28, 1)),
        tf.keras.layers.Dense(128,activation='relu'),
        tf.keras.layers.Dense(10, activation='softmax')
    ])

    # Compile the model
    model.compile(
        loss='sparse_categorical_crossentropy',
        optimizer=tf.keras.optimizers.Adam(0.001),
        metrics=['accuracy'],
    )

    # Train the model
    model.fit(
        ds_train,
        epochs=6,
        validation_data=ds_test,
    )

    # Save the model
    model.save("mnist_model")


if __name__== "__main__":
    main()