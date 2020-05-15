import tensorflow as tf
import numpy as np
import os

import sys

gpus = tf.config.experimental.list_physical_devices('GPU')

# Currently, memory growth needs to be the same across GPUs
for gpu in gpus:
    tf.config.experimental.set_memory_growth(gpu, True)

#tf.config.experimental.set_virtual_device_configuration(gpus[0], [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=1024)])



def representative_dataset_gen_factory(dataset_dir):
    # Open the npy file containing the input data samples
    input_data = np.load(dataset_dir)

    # Define the generator function that will feed samples of the input to the converter
    # The generator outputs a list containing a numpy array which has a single element of the data input
    # Note: The first dimension of the numpy array MUST be 1
    def representative_dataset_gen():
        for i in range(input_data.shape[0]):
            # Get sample input data as a numpy array in a method of your choosing.
            yield [np.expand_dims(input_data[i], axis = 0).astype("float32")]

    return representative_dataset_gen


def convert_to_tflite(saved_model_dir, reprentative_dataset_dir):
    # Instantiate a tf lite converter object to convert the saved model to a quantized uint8 tflite model
    converter = tf.compat.v1.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    converter.optimizations = [tf.lite.Optimize.DEFAULT]
    converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
    converter.inference_input_type = tf.uint8
    converter.inference_output_type = tf.uint8
    converter.representative_dataset = representative_dataset_gen_factory(reprentative_dataset_dir)
    tflite_quant_model = converter.convert()

    return tflite_quant_model

def edgetpu_compile(tflite_model_path):
    os.system("edgetpu_compiler {}".format(tflite_quant_model_path))



if __name__ == "__main__":
    # Parse command line arguments
    # The model save directory should be passed as an argument
    if(len(sys.argv) > 2):
        saved_model_dir = str(sys.argv[1])
        reprentative_dataset_dir = str(sys.argv[2])
    else:
        raise Exception("Must pass the saved model directory and the path to the representative dataset .npy file")

    # Convert model to a tflite model
    tflite_quant_model = convert_to_tflite(saved_model_dir, reprentative_dataset_dir)
    tflite_quant_model_path = "{}.tflite".format(saved_model_dir)
    open(tflite_quant_model_path, "wb").write(tflite_quant_model)

    # Use edgeTPU_compiler to compile model for TPU
    edgetpu_compile(tflite_quant_model_path)



