"""Provides a command-line interface and python API for deploying a model to the Google Coral board.

Currently, this script is setup to deploy the model via ssh. Therefore, it requires the address of the coral board
and that you have a key or password to access it. Once the model is deployed to the coral, it will also publish
a web server to display the results. The deploy script also only handles classification problems, support for more
model types is in the pipeline. The python API exposes a deploy function. If called from the command line, you must
pass a model (using -m argument), the address of the coral (-a), and EITHER an identity file (-i) OR a password (-p).

    Typical usage example:

    python3 deploy.py -m foo/model_quantized.tflite -a x.x.x.x -i ~/id_rsa
"""

from paramiko import SSHClient
from scp import SCPClient
import argparse
import os
from mdt.discoverer import Discoverer
from learn_ml.utils.log_configurator import LogConfigurator

DEFAULT_USERNAME = "mendel"
DEFAULT_PASSWORD = "mendel"

# Instantiate LogConfigurator
log_config = LogConfigurator(verbosity = "INFO", output_to_logfile = False)

# Get the logger for module
logger = log_config.get_logger(__name__)

def deploy(address, task, identity_file=None, password=None):
    """ Deploys the a model to the Coral Board.

    Connects to the coral board via ssh to deploy the model. You must pass a tflite model.
    For maximum performance, you should pass a quantized tflite model, which can be generated
    using the convert_to_edgetpu module. After deploying the model, the function will start
    a webserver publishing the results.


    Args:
        address: Address of the coral board
        model: Path to the tflite model to deploy
        identity_file: [Optional] Path to the identity file. Identity file must be provided
            if password is not provided.
        password: [Optional] Password to use for ssh authentication. Password must be provided
            if identity_file is not provided.
    Returns:
        None
    """

    # Flag for whether or not authenticating with key
    use_key = False
    if(identity_file is not None):
        use_key = True
    elif(password is None):
        raise Exception("Must pass identity file OR password")

    ssh = SSHClient()
    ssh.load_system_host_keys()

    # Connect to coral
    logger.info("Connecting to Anything Sensor...")
    if(use_key):  # Connect using private key
        ssh.connect(hostname=address, username=DEFAULT_USERNAME, key_filename=identity_file)
    else:  # Connect using password
        ssh.connect(hostname=address, username=DEFAULT_USERNAME, password=password)
    logger.info("Successfully connected to Anything Sensor v1!")

    # # Transfer model to coral
    # logger.info("Transferring model to Anything Sensor...")
    # # SCPCLient takes a paramiko transport as an argument
    # with SCPClient(ssh.get_transport()) as scp:
    #     scp.put(model, "/home/mendel/learn_ml/coral_inference/classification/" + os.path.basename(model))
    # logger.info("Transfer Successful!")

    # Start model execution
    ssh.exec_command("pkill screen")
    ssh.exec_command("cd /home/mendel/learn_ml/coral_inference/ && screen -d -m python3 "
                     + "app.py --task {task} -p spi ".format(task=task))

    logger.info("Started execution!")
    # logger.info("Stream accessible at {}:5000".format(address))

    ssh.close()

def deploy_usb(task):
    # Import a discoverer object from mendel development tools
    discoverer = Discoverer()

    # Discover available objects and get available devices
    discoverer.discover()
    discoveries = discoverer.discoveries

    # TODO Update this to allow for selecting between multiple available devices
    if(list(discoveries) != []):
        # Just select the first element in the dictionary
        ip = discoveries[list(discoveries)[0]]
        logger.info("Found Anything Sensor at {}!".format(ip))
        deploy(ip, task, password = DEFAULT_PASSWORD)


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--task', help="The task to run inference", required=True)
    parser.add_argument('-m', '--model', help='Path to .tflite model file', required=False)
    parser.add_argument('-a', '--address', help='Address of the coral device', required=False)
    parser.add_argument('-i', '--identity-file',
                        help='Identity file to authenticate with', required=False)
    parser.add_argument('-p', '--password', help='Password to login with', required=False)
    parser.add_argument('-u', '--usb', help='Deploy over USB', required=False, action = 'store_true')
    args = parser.parse_args()

    if(args.usb):
        deploy_usb(args.task)
    else:
        deploy(args.address, args.model, identity_file=args.identity_file, password=args.password)
