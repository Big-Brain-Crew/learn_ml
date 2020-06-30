from pose_estimation.pose_camera import PoseCamera
from pose_estimation.pose_estimator import PoseEstimator
MODEL='pose_estimation/posenet/models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite'

def main():
    pose_estimator = PoseEstimator(model=MODEL, stream=False)

    while True:
        print(pose_estimator.get_data())
        print(pose_estimator.get_length())


if __name__== "__main__":
    main()
