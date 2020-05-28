""" API for preparing model to deploy to Google Coral board.

This script will accept a tf2 saved model and convert it into a quantized tflite model.
After converting it, it will convert the model using the edge_tpu compiler tool.
In addition to a command line interface, it also publishes a python API. To quantize the
model, the script also requires a small, representative dataset to determine the input
ranges. Tensorflow documentation says the dataset can be as small as 12 examples, but
we recommend around 100. The dataset is accepted as a .npy file, containing an array
of inputs in the same shape as you pass to the model.

    Typical usage example:
    python3 convert_to_edgetpu.py foo/tf2_model bar/repr_dataset.npy
"""

import tensorflow as tf
import numpy as np
import os
import argparse
import sys


def _representative_dataset_gen_factory(dataset_dir):
    """ Creates a generator for elements of the representative dataset.

    Helper function for creating a generator for the tflite converter.

    Args:
        dataset_dir: Path to the .npy file containing the representative dataset.
            This np array should contain multiple input examples.
    Returns:
        A generator function that can be passed directly to the tflite converter.
    """

    # Open the npy file containing the input data samples
    input_data = np.load(dataset_dir)

    # Define the generator function that will feed samples of the input to the converter
    # The generator outputs a list containing a numpy array which has a single element of the data input
    # Note: The first dimension of the numpy array MUST be 1
    def representative_dataset_gen():
        for i in range(input_data.shape[0]):
            # Get sample input data as a numpy array in a method of your choosing.
            yield [np.expand_dims(input_data[i], axis=0).astype("float32")]

    return representative_dataset_gen


def _convert_to_tflite(saved_model_dir, representative_dataset_dir, use_tf1=False):
    """ Converts the model to a fully 8-bit integer quantized tflite model.

    By default, uses the tf2 converter to convert the model to a tflite model. This uses the
    post-training quantization scheme, which requires a representative dataset to
    quantize the model. If specified, it will use the tf1 converter

    Args:
        saved_model_dir: Path to directory containing the tf2 saved model
        representative_dataset_dir: Path to the .npy file containing the
            representative dataset. This np array should contain multiple
            input examples.
        use_tf1 (optional): True to use the tf1 converter. False will use the tf2 converter.
    Returns:
        A tflite_quantized model, which must be written to a file

    """

    if use_tf1:
        converter = tf.compat.v1.lite.TFLiteConverter.from_saved_model(saved_model_dir)
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
        converter.representative_dataset = _representative_dataset_gen_factory(representative_dataset_dir)
        tflite_quant_model = converter.convert()

    else:
        converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)

        # This enables quantization
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_types = [tf.int8]

        # This ensures that if any ops can't be quantized, the converter throws an error
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        
        # This sets the representative dataset so we can quantize the activations
        converter.representative_dataset = _representative_dataset_gen_factory(
            representative_dataset_dir)
        tflite_quant_model = converter.convert()

    return tflite_quant_model


def _edgetpu_compile(tflite_model_path):
    """ Run the edgetpu_compile script for the quantized tflite model.

    The function will write the edgetpu compiled model to [MODEL_NAME]_edgetpu.tflite.
    Currently, this function only works on debian systems.

    Args:
        tflite_model_path: Path to the quantized .tflite model
    Returns:
        None
    """
    os.system("edgetpu_compiler {}".format(tflite_model_path))


def convert_and_compile(saved_model_dir, representative_dataset_dir, use_tf1=False):
    """ Converts the model to tflite and compiles for edgetpu.

    This function will convert a tf2 saved model to a model compiled for the edgetpu.
    Once generated, the model will be saved to the file [MODEL NAME]_edgetpu.tflite

    Args:
        saved_model_dir: Path to directory containing the tf2 saved model
        representative_dataset_dir: Path to the .npy file containing the
            representative dataset. This np array should contain multiple
            input examples.
        use_tf1 (optional): True to use the tf1 converter. False will use the tf2 converter.
    Returns:
        None
    """

    # Set memory growth for GPU
    gpus = tf.config.experimental.list_physical_devices('GPU')
    for gpu in gpus:
        tf.config.experimental.set_memory_growth(gpu, True)

    # Convert model to a tflite model
    tflite_quant_model = _convert_to_tflite(saved_model_dir, representative_dataset_dir, use_tf1)
    tflite_quant_model_path = "{}.tflite".format(saved_model_dir)
    open(tflite_quant_model_path, "wb").write(tflite_quant_model)

    # Use edgeTPU_compiler to compile model for TPU
    _edgetpu_compile(tflite_quant_model_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--model", help="Path to model folder.", required=True, type=str)
    parser.add_argument("-r", "--representative", help="Path to representative dataset numpy file.",
                        required=True, type=str)
    parser.add_argument("-t", "--use_tf1", help="Bool; Whether to use the TF2 or TF1 converter",
                        default=False, type=bool)
    args = parser.parse_args()
    saved_model_dir = args.model
    representative_dataset_dir = args.representative
    use_tf1 = args.use_tf1

    convert_and_compile(saved_model_dir, representative_dataset_dir, use_tf1)
