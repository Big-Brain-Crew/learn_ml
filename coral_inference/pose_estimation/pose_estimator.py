from pose_estimation.pose_classifier import PoseClassifier
from pose_estimation.pose_camera import PoseCamera
import numpy as np
class PoseEstimator(object):

    def __init__(self,
                 model=None,
                 stream=False,
                 videosrc=1,
                 res='640x480',
                 score_threshold=0.1):
        if stream:
            self.pose_estimator = PoseCamera(model=model,
                                             res=res)
        else:
            self.pose_estimator = PoseClassifier(model=model, 
                                                 videosrc=videosrc,
                                                 res=res)

        self.score_threshold = score_threshold
        self.poses = []
        self.length = 17 * 3
        self.flattened_poses = np.zeros(self.length, dtype=np.float32)
        
    def get_data(self):
        if isinstance(self.pose_estimator, PoseClassifier):
            self.update_poses()
            return self.flattened_poses

        else:
            raise Exception("Must pass stream=False to receive pose data")

    def update_poses(self):
        self.poses = self.pose_estimator.get_frame()

        i = 0
        if self.poses:
            for pose in self.poses:
                for label, keypoint in pose.keypoints.items():
                    self.flattened_poses[3 * i] = keypoint.yx[1]
                    self.flattened_poses[3 * i + 1] = keypoint.yx[0]
                    self.flattened_poses[3 * i + 2] = keypoint.score
                    i = i + 1
                break
        else:
            self.flattened_poses = np.zeros(self.length)


    def get_length(self):
        self.update_poses()
        return self.length


