import os
import cv2
from coral_inference.classification.base_classifier import BaseClassifier
import time

import tflite_runtime.interpreter as tflite
import numpy as np

class Classifier(BaseClassifier):
    video_source = 1

    def __init__(self, model_path):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            self.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))

        # Load TFLite model and allocate tensors
        self.interpreter = tflite.Interpreter(model_path=model_path, experimental_delegates=[tflite.load_delegate('libedgetpu.so.1.0')])
        self.interpreter.allocate_tensors()
        super(Classifier, self).__init__()

    def set_video_source(self, source):
        self.video_source = source

    # Crops an image into a square.
    # image: image to be cropped.
    # target_dims: Output dimensions. Expected as a 2D list.
    # i.e. to output a RGB image of size (28,28,3), pass [28,28].
    def crop_resize_square(self, img, target_dims):
        # Get the shape of the input image
        input_dims = img.shape

        # Get the smallest input dimension
        smallest_dim_idx = np.argmin(input)

        # Get the start and end indices to crop at
        width_crop_start = int((input_dims[0] - input_dims[smallest_dim_idx])/2)
        width_crop_end   = int(input_dims[0] - width_crop_start)
        height_crop_start = int((input_dims[1] - input_dims[smallest_dim_idx])/2)
        height_crop_end   = int(input_dims[1] - height_crop_start)

        # Crop the image
        cropped = img[width_crop_start:width_crop_end, height_crop_start: height_crop_end]

        # Return resized image
        return cv2.resize(cropped, dsize=tuple(target_dims))

    # Conver the image to gray scale
    def convert_to_gray(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Format the image to match the graph tensor input
    # Either (1, X, Y) or (1, X, Y, 1)
    def format_input(self, img,  input_details):

        input_shape = input_details[0]['shape']

        # Add first dimension
        input_data = np.expand_dims(img, axis = 0)

        # Add end dimension if model expects it
        if input_shape.shape[0] > 3 and input_shape[3] == 1:
            input_data = np.expand_dims(input_data, axis=3)

        # Convert input to float if model expects it
        # This is necessary for tf2 models
        if input_details[0]['dtype'] == np.float32:
            input_data = input_data.astype(np.float32)

        return input_data

    def frames(self):
        # Get input and output tensors
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        input_shape = input_details[0]['shape']

        # Open camera capture
        camera = cv2.VideoCapture(self.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            start = time.time()

            # read current frame
            _, img = camera.read()
            original_img = img.copy()

            # Perform image preprocessing
            img = self.preprocess(img, input_shape)

            # Format the image as tensor input
            input_data = self.format_input(img, input_details)

            # Set the image as the input tensor
            self.interpreter.set_tensor(input_details[0]['index'], input_data)

            # Perform inference
            self.interpreter.invoke()

            # The function `get_tensor()` returns a copy of the tensor data.
            # Use `tensor()` in order to get a pointer to the tensor.
            probabilities = np.squeeze(self.interpreter.get_tensor(output_details[0]['index']))

            # The result is the maximum probability
            result = np.argmax(probabilities)

            # Display result on original image
            cv2.putText(original_img, str(result), (0,100), cv2.FONT_HERSHEY_SIMPLEX, 4, (255, 255, 0), 2, cv2.LINE_AA)

            # encode
            yield cv2.imencode('.jpg', original_img)[1].tobytes()


    # Perform all required image preprocessing. Should be implemented by child class.
    def preprocess(self, img, input_shape):
        pass

# Number classifier trained on the MNIST digits dataset.
class MnistClassifier(Classifier):
    def __init__(self, model_path):
        super(MnistClassifier, self).__init__(model_path)

    # The MNIST dataset consists of white numbers on a black background.
    # The camera image must be cropped to a square, resized, and converted
    # to a similar black background and white number.
    def preprocess(self, img, input_shape):

        # Model expects square images
        img = self.crop_resize_square(img, input_shape[1:3])

        # Image needs to be black and white
        # Input tensor may be of the shape (1,X,Y) or (1,X,Y,dim)
        if input_shape.shape[0] < 4 or input_shape[3] == 1:
            img = self.convert_to_gray(img)

        # Threshold
        _, img = cv2.threshold(img, 127, 255, cv2.THRESH_OTSU)

        # Invert
        img = cv2.bitwise_not(img)

        # Normalize the image
        img = img / 255.0

        return img
