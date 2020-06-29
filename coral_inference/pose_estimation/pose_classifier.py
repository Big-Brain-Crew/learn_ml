import os
import argparse
import collections
from functools import partial
import re
import time

import numpy as np
from PIL import Image
import svgwrite

from posenet import gstreamer
from posenet.pose_engine import PoseEngine
import cv2
from ..classification.base_classifier import BaseClassifier

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

    def __init__(self, model=None):

        default_model = 'coral_inference/pose_estimation/posenet/models/mobilenet/posenet_mobilenet_v1_075_%d_%d_quant_decoder_edgetpu.tflite'
        if self.res == '480x360':
            self.src_size = (640, 480)
            # self.appsink_size = (480, 360)
            self.model = model or default_model % (353, 481)
        elif self.res == '640x480':
            self.src_size = (640, 480)
            # self.appsink_size = (640, 480)
            self.model = model or default_model % (481, 641)
        elif self.res == '1280x720':
            self.src_size = (1280, 720)
            # self.appsink_size = (1280, 720)
            self.model = model or default_model % (721, 1281)

        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            self.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))

        self.engine = PoseEngine(self.model)

        super(PoseClassifier, self).__init__()

    def set_video_source(self, source):
        self.video_source = source

    def preprocess(self, img):

        img = cv2.resize(img, self.src_size)

        return img

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
            poses, inference_time = engine.DetectPosesInImage(img)
            print("Inference time: {}".format(inference_time))
            
            for pose in poses:
                if pose.score < 0.4: continue
                print('\nPose Score: ', pose.score)
                for label, keypoint in pose.keypoints.items():
                    print(' %-20s x=%-4d y=%-4d score=%.1f' %
                        (label, keypoint.yx[1], keypoint.yx[0], keypoint.score))
            # encode
            yield 0
