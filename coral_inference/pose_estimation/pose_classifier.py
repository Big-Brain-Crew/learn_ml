import os
import argparse
import collections
from functools import partial
import re
import time

import numpy as np
from PIL import Image
import svgwrite

#from pose_estimation.posenet import gstreamer
from pose_estimation.posenet.pose_engine import PoseEngine
import cv2
from classification.base_classifier import BaseClassifier

EDGES = (
    ('nose', 'left eye'),
    ('nose', 'right eye'),
    ('nose', 'left ear'),
    ('nose', 'right ear'),
    ('left ear', 'left eye'),
    ('right ear', 'right eye'),
    ('left eye', 'right eye'),
    ('left shoulder', 'right shoulder'),
    ('left shoulder', 'left elbow'),
    ('left shoulder', 'left hip'),
    ('right shoulder', 'right elbow'),
    ('right shoulder', 'right hip'),
    ('left elbow', 'left wrist'),
    ('right elbow', 'right wrist'),
    ('left hip', 'right hip'),
    ('left hip', 'left knee'),
    ('right hip', 'right knee'),
    ('left knee', 'left ankle'),
    ('right knee', 'right ankle'),
)


class PoseClassifier(BaseClassifier):

    def __init__(self, model=None, videosrc=1, res='640x480', stream = False):
        self.stream = stream
        self.res = res
        default_model = 'pose_estimation/posenet/models/mobilenet/posenet_mobilenet_v1_075_%d_%d_quant_decoder_edgetpu.tflite'
        if self.res == '480x360':
            self.src_size = (640, 480)
            self.model = model or default_model % (353, 481)
        elif self.res == '640x480':
            self.src_size = (640, 480)
            self.model = model or default_model % (481, 641)
        elif self.res == '1280x720':
            self.src_size = (1280, 720)
            self.model = model or default_model % (721, 1281)

        self.video_source = videosrc
        self.engine = PoseEngine(self.model)

        super(PoseClassifier, self).__init__()

    def preprocess(self, img):

        img = cv2.resize(img, self.src_size)

        return img

    def get_length(self):
        return 51

    def frames(self):

        # Open camera capture
        camera = cv2.VideoCapture(self.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        while True:
            start = time.time()

            # read current frame
            _, img = camera.read()

            # Perform image preprocessing
            img = self.preprocess(img)

            # Run inference
            poses, inference_time = self.engine.DetectPosesInImage(img)

            if(self.stream):
                if(len(poses) > 0):
                    pose = poses[0]
                    for label, keypoint in pose.keypoints.items():
                        # Display result on original image
                        if(keypoint.score > 0.5):
                            img = cv2.circle(img, (keypoint.yx[1], keypoint.yx[0]), 4, (255, 255, 0), 2)

                yield cv2.imencode('.jpg', img)[1].tobytes()
            else:
                output_data = np.zeros(shape = (self.get_length(),), dtype = np.float32)
                if poses:
                    pose = poses[0]
                    for i, (label, keypoint) in enumerate(pose.keypoints.items()):
                        output_data[3 * i] = keypoint.yx[1]
                        output_data[3 * i + 1] = keypoint.yx[0]
                        output_data[3 * i + 2] = keypoint.score

                yield output_data
