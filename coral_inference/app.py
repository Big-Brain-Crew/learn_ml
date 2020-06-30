import argparse
from periphery import GPIO

from SPIComms import SPIComms
from pose_estimation.pose_estimator import PoseEstimator 
# from classification.FaceCamera import FaceCamera

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-t","--task", help="Task for neural net to accomplish", required=True)
    parser.add_argument("-p","--comm-protocol", help="Communication protocol over which to transmit data, currently only supports \"spi\"", required=True)
    args = parser.parse_args()

    print("Initializing neural net")

    if(args.task == 'posenet'):
        nn = PoseEstimator(stream = (args.comm_protocol == "video"))
    else:
        nn = PoseEstimator(stream = (args.comm_protocol == "video"))
        # nn = FaceCamera(args.model, stream = (args.comm_protocol == "video"))
    data_length = nn.get_length()

    print("Initializing comms")
    comm_handler = None

    # Streaming data over SPI
    if(args.comm_protocol == "spi"):
        comm_handler = SPIComms(data_length)
        comm_handler.start_comms()

        while(True):
            comm_handler.set_data(nn.get_data())

    else: # If we're streaming video, just loop forever to play the stream
        while True:
            pass


if __name__ == "__main__":
    # Create the GPIO pin for the indicator light and turn it on
    indicator_light = GPIO(6, "out")
    indicator_light.write(True)

    try:
        main()
    except:
        indicator_light.write(False)
        indicator_light.close()



