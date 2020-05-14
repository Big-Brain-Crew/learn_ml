import tensorflow as tf
import tensorflow_datasets as tfds
import PIL

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

    image = Image.open(args.input).convert('L').resize((28, 28), Image.ANTIALIAS)
    image = np.expand_dims(np.array(image), 2)

    interpreter = tf.lite.Interpreter('mnist_quant_edgetpu.tflite')
    interpreter.allocate_tensors()

    # Collect all inference predictions in a list
    batch_prediction = []

    prediction = classify_image(interpreter, image)
    batch_prediction.append(prediction)

    # Compare all predictions to the ground truth
    tflite_accuracy = tf.keras.metrics.Accuracy()
    tflite_accuracy(batch_prediction, batch_truth)
    print("Quant TF Lite accuracy: {:.3%}".format(tflite_accuracy.result()))

if __init__ == "__main__":
    main()
