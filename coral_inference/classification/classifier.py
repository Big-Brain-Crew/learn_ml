import os
import cv2
from base_classifier import BaseClassifier
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

    def crop_resize_square(self, image, target_dims):
        # Get the shape of the input image
        input_dims = image.shape

        # Get the smallest input dimension
        smallest_dim_idx = np.argmin(input)

        # Get the start and end indices to crop at
        width_crop_start = int((input_dims[0] - input_dims[smallest_dim_idx])/2)
        width_crop_end   = int(input_dims[0] - width_crop_start)
        height_crop_start = int((input_dims[1] - input_dims[smallest_dim_idx])/2)
        height_crop_end   = int(input_dims[1] - height_crop_start)

        # Crop the image
        cropped = image[width_crop_start:width_crop_end, height_crop_start: height_crop_end]
        print(target_dims)
        # Return resized image
        return cv2.resize(cropped, tuple(target_dims))

    def convert_to_gray(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def frames(self):
        # Get input and output tensors
        input_details = self.interpreter.get_input_details()
        output_details = self.interpreter.get_output_details()

        input_shape = input_details[0]['shape']

        camera = cv2.VideoCapture(self.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            start = time.time()
            # read current frame
            _, img = camera.read()

            img = self.crop_resize_square(img, input_shape[1:])

            # Image needs to be black and white
            if(input_shape.shape[0] < 4):
                img = self.convert_to_gray(img)


            # Test model on random input data
            input_data = np.expand_dims(img, axis = 0)
            self.interpreter.set_tensor(input_details[0]['index'], input_data)

            self.interpreter.invoke()

            # The function `get_tensor()` returns a copy of the tensor data.
            # Use `tensor()` in order to get a pointer to the tensor.
            probabilities = np.squeeze(self.interpreter.get_tensor(output_details[0]['index']))

            result = np.argmax(probabilities)

            img = cv2.resize(img, (100,100))
            cv2.putText(img, str(result), (0,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

            # encode
            yield cv2.imencode('.jpg', img)[1].tobytes()
