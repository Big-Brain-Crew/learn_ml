#!/usr/bin/env python
from flask import Flask, render_template, Response
import cv2
import argparse
import json
import pipeline_factory
import camera

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--task',
                        help="Inference task being performed", required=True)
    parser.add_argument('-p', '--param_config',
                        help="Path to JSON file with parameters", required=True)
    args = parser.parse_args()

    app = Flask(__name__)

    # Choose the classifier based on the model type.
    def get_stream():
        config = json.load(open(args.param_config))
        params = config["app_params"]
        factory = pipeline_factory.get_instance(args.task)
        pipeline = factory.create_pipeline(params)
        return pipeline

    # Define index page

    @app.route('/')
    def index():
        return render_template('index.html')

    # Define generator function that yields frames from the classifier
    # The classifier is responsible for capturing a frame from the camera, processing it, and returning the results

    def gen(source):
        while True:
            pred = source.get_prediction()
            # print(pred)
            frame = source.get_output_frame_bytes()
            # frame = cv2.imencode('.jpg', next(source))[1].tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    # Define the video feed on the webpage

    @app.route('/video_feed')
    def video_feed():
        cam = get_stream()
        cam.start()

        return Response(gen(cam),
                        mimetype='multipart/x-mixed-replace; boundary=frame')

    app.run(host='0.0.0.0', debug=True)
