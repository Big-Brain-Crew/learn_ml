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


def main(args):

    config = json.load(open(args.param_config))
    params = config["app_params"]

    if params["stream_flask"]:

        # Run a separate script that creates a Flask app. This is temporary - long term, multiple
        # data streams will be run from a single script.
        subprocess.run('python3 flask_app.py -t detection -p {}'.format(args.param_config),
                       shell=True)
                       
    else:

        factory = pipeline_factory.get_instance(args.task)

        pipeline = factory.create_pipeline(params)

        # Start inference
        pipeline.start()

        while True:
            time.sleep(0)  # Keep running while data is streaming


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--task',
                        help="Inference task being performed", required=True)
    parser.add_argument('-p', '--param_config',
                        help="Path to JSON file with parameters", required=True)

    args = parser.parse_args()
    main(args)
