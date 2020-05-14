import tensorflow as tf
import tensorflow_datasets as tfds
import png

assert tf.__version__.startswith('2')

import os
import numpy as np
import matplotlib.pyplot as plt

IMAGE_SIZE = 28
BATCH_SIZE = 128

def normalize_img(image, label):
    """Normalizes images: `uint8` -> `float32`."""
    return tf.cast(image, tf.float32) / 255., label

def set_input_tensor(interpreter, input):
    input_details = interpreter.get_input_details()[0]
    tensor_index = input_details['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = input
    # NOTE: This model uses float inputs, but if inputs were uint8,
    # we would quantize the input like this:
    #   scale, zero_point = input_details['quantization']
    #   input_tensor[:, :] = np.uint8(input / scale + zero_point)

def classify_image(interpreter, input):
    set_input_tensor(interpreter, input)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = interpreter.get_tensor(output_details['index'])
    # NOTE: This model uses float outputs, but if outputs were uint8,
    # we would dequantize the results like this:
    #   scale, zero_point = output_details['quantization']
    #   output = scale * (output - zero_point)
    top_1 = np.argmax(output)
    return top_1

def main():

    # Load the MNIST dataset
    (ds_train, ds_test), ds_info = tfds.load('mnist',
                                            split=['train', 'test'],
                                            shuffle_files=True,
                                            as_supervised=True,
                                            with_info=True)

    # Preprocess train dataset
    ds_train = ds_train.map(normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    ds_train = ds_train.cache()

    # Preprocess test dataset
    ds_test = ds_test.map(normalize_img, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    ds_test = ds_test.batch(128)
    ds_test = ds_test.cache()
    ds_test = ds_test.prefetch(tf.data.experimental.AUTOTUNE)

    # Evaluate and compare the raw and quantized models
    batch_images, batch_labels = next(iter(ds_test))

    # Load normal TF model
    model = tf.keras.models.load_model("model")

    # Run inference
    logits = model(batch_images)
    prediction = np.argmax(logits, axis=1)
    truth = batch_labels

    # Evaluate accuracy
    keras_accuracy = tf.keras.metrics.Accuracy()
    keras_accuracy(prediction, truth)
    print("Raw model accuracy: {:.3%}".format(keras_accuracy.result()))

    # Load TFLite model
    interpreter = tf.lite.Interpreter('mnist_quant.tflite')
    interpreter.allocate_tensors()

    # Collect all inference predictions in a list
    batch_prediction = []
    batch_truth = batch_labels

    # Run inference
    for i in range(len(batch_images)):
        prediction = classify_image(interpreter, batch_images[i])
        batch_prediction.append(prediction)

    # Compare all predictions to the ground truth
    tflite_accuracy = tf.keras.metrics.Accuracy()
    tflite_accuracy(batch_prediction, batch_truth)
    print("Quant TF Lite accuracy: {:.3%}".format(tflite_accuracy.result()))

if __name__ == "__main__":
    main()