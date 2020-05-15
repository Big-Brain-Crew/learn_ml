#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
from classifier import Classifier




# Instantiate a Flask app
app = Flask(__name__)


# Define index pag
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
    return Response(gen(Classifier("classification_model.tflite")),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)