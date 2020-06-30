import os
import argparse
import collections
from functools import partial
import re
import time

import numpy as np
from PIL import Image
import svgwrite

from pose_estimation.posenet import gstreamer
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


class PoseCamera(object):

    def __init__(self, model=None, mirror=False,res='640x480',videosrc='/dev/video0',h264=False,jpeg=False):
        self.mirror = mirror
        self.res = res
        self.videosrc = videosrc
        self.h264 = h264
        self.jpeg = jpeg

        self.default_model = 'pose_estimation/posenet/models/mobilenet/posenet_mobilenet_v1_075_%d_%d_quant_decoder_edgetpu.tflite'
        if self.res == '480x360':
            self.src_size = (640, 480)
            self.appsink_size = (480, 360)
            self.model = model or self.default_model % (353, 481)
        elif self.res == '640x480':
            self.src_size = (640, 480)
            self.appsink_size = (640, 480)
            self.model = model or self.default_model % (481, 641)
        elif self.res == '1280x720':
            self.src_size = (1280, 720)
            self.appsink_size = (1280, 720)
            self.model = model or self.default_model % (721, 1281)

        self.run()


    def run(self):
        n = 0
        sum_process_time = 0
        sum_inference_time = 0
        ctr = 0
        fps_counter = self.avg_fps_counter(30)
        def run_inference(engine, input_tensor):
            return engine.run_inference(input_tensor)

        def render_overlay(engine, output, src_size, inference_box):
            nonlocal n, sum_process_time, sum_inference_time, fps_counter

            svg_canvas = svgwrite.Drawing('', size=src_size)
            start_time = time.monotonic()
            outputs, inference_time = engine.ParseOutput(output)
            end_time = time.monotonic()
            n += 1
            sum_process_time += 1000 * (end_time - start_time)
            sum_inference_time += inference_time

            avg_inference_time = sum_inference_time / n
            text_line = 'PoseNet: %.1fms (%.2f fps) TrueFPS: %.2f Nposes %d' % (
                avg_inference_time, 1000 / avg_inference_time, next(fps_counter), len(outputs)
            )

            self.shadow_text(svg_canvas, 10, 20, text_line)
            for pose in outputs:
                self.draw_pose(svg_canvas, pose, src_size, inference_box)
            return (svg_canvas.tostring(), False)

        self._run(run_inference, render_overlay)

    def shadow_text(self, dwg, x, y, text, font_size=16):
        dwg.add(dwg.text(text, insert=(x + 1, y + 1), fill='black',
                         font_size=font_size, style='font-family:sans-serif'))
        dwg.add(dwg.text(text, insert=(x, y), fill='white',
                         font_size=font_size, style='font-family:sans-serif'))

    def draw_pose(self, dwg, pose, src_size, inference_box, color='yellow', threshold=0.2):
        box_x, box_y, box_w, box_h = inference_box
        scale_x, scale_y = src_size[0] / box_w, src_size[1] / box_h
        xys = {}
        for label, keypoint in pose.keypoints.items():
            if keypoint.score < threshold:
                continue
            # Offset and scale to source coordinate space.
            kp_y = int((keypoint.yx[0] - box_y) * scale_y)
            kp_x = int((keypoint.yx[1] - box_x) * scale_x)

            xys[label] = (kp_x, kp_y)
            dwg.add(dwg.circle(center=(int(kp_x), int(kp_y)), r=5,
                               fill='cyan', fill_opacity=keypoint.score, stroke=color))

        for a, b in EDGES:
            if a not in xys or b not in xys:
                continue
            ax, ay = xys[a]
            bx, by = xys[b]
            dwg.add(dwg.line(start=(ax, ay), end=(bx, by), stroke=color, stroke_width=2))

    def avg_fps_counter(self, window_size):
        window = collections.deque(maxlen=window_size)
        prev = time.monotonic()
        yield 0.0  # First fps value.

        while True:
            curr = time.monotonic()
            window.append(curr - prev)
            prev = curr
            yield len(window) / sum(window)

    def _run(self, inf_callback, render_callback):
        
        print('Loading model: ', self.model)
        engine = PoseEngine(self.model)
        input_shape = engine.get_input_tensor_shape()
        inference_size = (input_shape[2], input_shape[1])

        gstreamer.run_pipeline(partial(inf_callback, engine), partial(render_callback, engine),
                               self.src_size, inference_size,
                               mirror=self.mirror,
                               videosrc=self.videosrc,
                               h264=self.h264,
                               jpeg=self.jpeg,
                               )
