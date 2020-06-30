
import os
import sys

from pose_estimation.pose_classifier import PoseClassifier
from pose_estimation.posenet.pose_engine import PoseEngine


# engine = PoseEngine("pose_estimation/posenet/models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite")

pose_classifier = PoseClassifier()
pose_score = 0.1

# Run inference
while True:

    poses = pose_classifier.get_frame()
    # print(poses)
    for pose in poses:
      if pose.score < 0.1: continue
      print('\nPose Score: ', pose.score)
      for label, keypoint in pose.keypoints.items():
          print(' %-20s x=%-4d y=%-4d score=%.1f' %
              (label, keypoint.yx[1], keypoint.yx[0], keypoint.score))


        # encode
        #yield 0
