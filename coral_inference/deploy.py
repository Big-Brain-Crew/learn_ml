from paramiko import SSHClient
from scp import SCPClient
import argparse

# Parse arguments
parser = argparse.ArgumentParser()
parser.add_argument('-m','--model', help='Path to .tflite model file', required=True)
parser.add_argument('-a','--address', help='Address of the coral device', required=True)
parser.add_argument('-i','--identity-file', help='Identity file to authenticate with', required=False)
parser.add_argument('-p','--password', help='Password to login with', required=False)
args = parser.parse_args()

# Flag for whether or not authenticating with key
use_key = False
if(args.identity_file is not None):
    use_key = True
elif(args.password is None): # This condition means that neither identity file nor password was passed
    raise Exception("Must pass identity file OR password")


ssh = SSHClient()
ssh.load_system_host_keys()

# Connect to coral
print("Connecting...")
if(use_key): # Connect using private key
    ssh.connect(hostname = args.address, username = "mendel", key_filename = args.identity_file)
else: # Connect using password
    ssh.connect(hostname = args.address, username = "mendel", password = args.password)
print("Successfully connected to Anything Sensor v1!")

# Transfer model to coral
print("Transferring model to Anything Sensor...")
# SCPCLient takes a paramiko transport as an argument
with SCPClient(ssh.get_transport()) as scp:
    scp.put(args.model, "/home/mendel/learn_ml/coral_inference/classification/classification_model.tflite")
print("Transfer Successful!")


# Start model execution
ssh.exec_command("pkill screen")
ssh.exec_command("cd /home/mendel/learn_ml/coral_inference/classification && screen -d -m python3 app.py")

print("Started execution!")
print("Stream accessible at {}:5000".format(args.address))

ssh.close()