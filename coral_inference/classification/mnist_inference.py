### ---------------------------------------------------------------------------- ###
#  This script runs inference on a saved image using a model trained
#  on the MNIST digit dataset. The main purpose of the script is to test 
#  performing inference on the Coral dev board using a TFLite Edge TPU compiled 
#  model. Later another script will be made to run live inference.
### ---------------------------------------------------------------------------- ###

import platform
from PIL import Image
import tflite_runtime.interpreter as tflite
import os
import numpy as np

EDGETPU_SHARED_LIB = {
  'Linux': 'libedgetpu.so.1',
  'Darwin': 'libedgetpu.1.dylib',
  'Windows': 'edgetpu.dll'
}[platform.system()]

# Create a TFLite Interpreter for running inference.
def make_interpreter(model_file):

  model_file, *device = model_file.split('@')

  return tflite.Interpreter(
      model_path=model_file,
      experimental_delegates=[
          tflite.load_delegate(EDGETPU_SHARED_LIB,
                               {'device': device[0]} if device else {})
      ])


# Set the input tensor to the intepreter
def set_input_tensor(interpreter, input):

    input_details = interpreter.get_input_details()[0]
    tensor_index = input_details['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:, :] = input

    # NOTE: This model uses float inputs, but if inputs were uint8,
    # we would quantize the input like this:
    #   scale, zero_point = input_details['quantization']
    #   input_tensor[:, :] = np.uint8(input / scale + zero_point)

# Run inference on an image
def classify_image(interpreter, input):

    set_input_tensor(interpreter, input)
    interpreter.invoke() # Calculate inference
    output_details = interpreter.get_output_details()[0]
    output = interpreter.get_tensor(output_details['index'])

    # NOTE: This model uses float outputs, but if outputs were uint8,
    # we would dequantize the results like this:
    #   scale, zero_point = output_details['quantization']
    #   output = scale * (output - zero_point)
    top_1 = np.argmax(output)
    return top_1


def main():

    # Load the image
    image = Image.open("images/digit.png").convert('L').resize((28, 28), Image.ANTIALIAS)
    image = np.expand_dims(np.array(image), 2)

    # Create the TFLite interpreter
    # This requires a tensorflow model that has been post-quantized, converted
    # to TFLite, and compiled for the edge TPU.
    interpreter = make_interpreter("models/mnist_quant_edgetpu.tflite")
    interpreter.allocate_tensors()

    # Perform inference
    prediction = classify_image(interpreter, image)
    print(prediction)


if __name__ == "__main__":
    main()
