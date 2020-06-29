from pose_camera import PoseCamera

MODEL='coral_inference/pose_estimation/posenet/models/mobilenet/posenet_mobilenet_v1_075_481_641_quant_decoder_edgetpu.tflite'

def main():
    pose_camera = PoseCamera(model=MODEL,use_stream=True)
    pose_camera.run()


if __name__== "__main__":
    main()
