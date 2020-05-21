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

def deploy(address, model, identity_file = None, password = None):
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
    elif(password is None): # This condition means that neither identity file nor password was passed
        raise Exception("Must pass identity file OR password")

    ssh = SSHClient()
    ssh.load_system_host_keys()

    # Connect to coral
    print("Connecting...")
    if(use_key): # Connect using private key
        ssh.connect(hostname = address, username = "mendel", key_filename = identity_file)
    else: # Connect using password
        ssh.connect(hostname = address, username = "mendel", password = password)
    print("Successfully connected to Anything Sensor v1!")

    # Transfer model to coral
    print("Transferring model to Anything Sensor...")
    # SCPCLient takes a paramiko transport as an argument
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(model, "/home/mendel/learn_ml/coral_inference/classification/" + model)
    print("Transfer Successful!")


    # Start model execution
    ssh.exec_command("pkill screen")
    ssh.exec_command("cd /home/mendel/learn_ml/coral_inference/classification && screen -d -m python3 app.py -m " + model)

    print("Started execution!")
    print("Stream accessible at {}:5000".format(address))

    ssh.close()

if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-m','--model', help='Path to .tflite model file', required=True)
    parser.add_argument('-a','--address', help='Address of the coral device', required=True)
    parser.add_argument('-i','--identity-file', help='Identity file to authenticate with', required=False)
    parser.add_argument('-p','--password', help='Password to login with', required=False)
    args = parser.parse_args()

    deploy(args.address, args.model, identity_file = args.identity_file, password = args.password)
