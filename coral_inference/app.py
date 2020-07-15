''' Main app for inference on the Coral Edge TPU board.

This app will run an inference pipeline that streams inference results to either the Arduino
over SPI or to a locally hosted video stream using Flask. The app currently supports any SSD
object detection model.

'''

import argparse
import time
import subprocess
import json
import pipeline_factory
from flask import Flask, render_template, Response, request
from flask_api import status


config = {
        "source": None,
        "engine": None,
        "postprocessor": None,
        "stream_spi": False,
        "stream_flask": False
}


app = Flask(__name__)


@app.route('/update_config', methods=["POST"])
def update_config():
    global config
    global pipeline

    config = request.get_json()["app_params"]
    pipeline = factory.create_pipeline(config)
    pipeline.start()

    return {}

@app.route('/')
def index():
    if(config["stream_flask"] == True):
        return render_template('index.html')
    else:
        return {}, status.HTTP_204_NO_CONTENT


def gen(source):
    while True:
        frame = source.get_output_frame_bytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



@app.route('/video_feed')
def video_feed():
    global pipeline

    if(config["stream_flask"] == True):
        return Response(gen(pipeline),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
    else:
        return {}, status.HTTP_204_NO_CONTENT



if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument('-t', '--task',
    #                     help="Inference task being performed", required=True)
    # parser.add_argument('-p', '--param_config',
    #                     help="Path to JSON file with parameters", required=True)

    # args = parser.parse_args()

    # config = json.load(open(args.param_config))
    # params = config["app_params"]

    factory = pipeline_factory.get_instance("detection")

    pipeline = None

    app.run(host='0.0.0.0', debug=True)


