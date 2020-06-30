#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
from classification import classifier
from pose_estimation import pose_classifier
import argparse

if __name__ == '__main__':
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--model', help='Path to .tflite model file', required=True)
    parser.add_argument("--mnist", required=False, action="store_true")
    parser.add_argument("--face", required=False, action="store_true")
    parser.add_argument("--pose", required=False, action="store_true")
    args = parser.parse_args()

    app = Flask(__name__)



    # Choose the classifier based on the model type
    def choose_classifier(model_type):

        if model_type == "mnist":
            return classifier.MnistClassifier(args.model)
        elif model_type == "face":
            return classifier.FaceClassifier(args.model, True)
        elif model_type == "pose":
            return pose_classifier.PoseClassifier(videosrc = 0, stream = True)
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
        #model_type = args.model.split('/')[-1].split('_')[0]
        if(args.mnist):
            model_type = "mnist"
        elif(args.face):
            model_type = "face"
        elif(args.pose):
            model_type = "pose"
        else:
            model_type = "other"

        print(model_type)
        classifier_obj = choose_classifier(model_type)
        print(classifier_obj)
        return Response(gen(classifier_obj),
                        mimetype='multipart/x-mixed-replace; boundary=frame')


    app.run(host='0.0.0.0', debug=True)
