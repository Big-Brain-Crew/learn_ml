#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
from classifier import Classifier
import classifier
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-m','--model', help='Path to .tflite model file', required=True)
args = parser.parse_args()


# Instantiate a Flask app
app = Flask(__name__)

# Choose the classifier based on the model type
def choose_classifier(model_type):

    if model_type == "mnist":
        return classifier.MnistClassifier(args.model)
    else:
        return classifier.Classifier(args.model)


# Define index page
@app.route('/')
def index():
    return render_template('index.html')

# Define generator function that yields frames from the classifier
# The classifier is responsible for capturing a frame from the camera, processing it, and returning the results
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# Define the video feed on the webpage
@app.route('/video_feed')
def video_feed():
     
    # Choose classifier
    model_type = args.model.split('/')[-1].split('_')[0]
    print(model_type)
    classifier_obj = choose_classifier(model_type)
    print(classifier_obj)
    return Response(gen(classifier_obj),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
