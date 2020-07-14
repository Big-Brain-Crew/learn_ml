from periphery import SPI, GPIO
import time

import threading

import numpy as np

class SPIComms(object):
    # Message headers defined for this communication protocl
    HEADERS = {
        "heartbeat" : b'\x10',
        "message" : b'\x20',
        "config" : b'\x30'
    }

    def __init__(self, source):
        self.source = source
        self.data_length = self.source.get_flatten_length()

        # Store heartbeat received from microcontroller
        # Used to make sure that microcontroller is still available
        self.prev_heartbeat_count = 0
        self.heartbeat_count = 0

        # Create the data format message
        # Message is 4 bytes long
        # Defined in communication doc
        self.data_format_message = [0, self.data_length, 0, 0]

        self.spi = None
        self.signal_pin = None
        self.comm_thread = None

        self.max_error_count = 50

        self.data_lock = threading.Lock()
        self.data = np.zeros(shape = (self.data_length,), dtype = np.float32)

    def start(self):
        # Open spidev0.0 device with mode 0 and max speed 100 kHz
        if(self.spi is None):
            self.spi = SPI("/dev/spidev0.0", 0, 30000) #, bit_order= "lsb")

        # Open GPIO pin connection
        if(self.signal_pin is None):
            self.signal_pin = GPIO(6, "in")

        if(self.comm_thread is None):
            print("starting comms thread")
            self.comm_thread = threading.Thread(target=self._comm_thread_fn, daemon = True)
            self.comm_thread.start()

    def set_data(self, data):
        with self.data_lock:
            np.copyto(self.data, data)

    def _comm_thread_fn(self):
        while True:
            # Initialize the communications with the microcontoller
            self._comm_init()
            error_count = 0
            while error_count < self.max_error_count:
                

                # heartbeat header
                self.prev_heartbeat_count = self.heartbeat_count
                self.heartbeat_count = int.from_bytes(self.spi.transfer(self.HEADERS["heartbeat"]), "little")

                if(self.heartbeat_count <= self.prev_heartbeat_count):
                    print("ERROR")
                    error_count += 1
                else:
                    error_count = 0

                if(self.signal_pin.read()):
                    print("Transferring data")
                    self.spi.transfer(self.HEADERS['message'])
                    with self.data_lock:
                        self.data = self.source.tobytes()
                        self.spi.transfer(self.data)

                time.sleep(0.01)

    def _comm_init(self):
        # Flags to store where in the comm init program is
        init_signal_received = False

        print("Starting init")

        # Create an array storing the responses received from the microcontroller
        responses = [b'\x00', b'\x00', b'\x00']

        # Loop init process
        while not init_signal_received:
            # Pop the first response and append the last response
            responses.pop(0)
            responses.append(self.spi.transfer(b'\xFF'))

            startTime = time.time()

            # Read pin for 100 ms to check for correct response
            # Correct response is high on the signal pin and 0xFF, 0xFE, 0xFD heartbeat sequence
            while time.time() - startTime < 0.1:
                if(self.signal_pin.read() and responses == [b'\xff', b'\xfe', b'\xfd']):
                    init_signal_received = True
                    break

        print("Received signal, waiting for heartbeat")
        self.spi.transfer(self.HEADERS["config"])
        responses = self.spi.transfer(b'\x00\x00\x00\x00')

        # Store the last two heartbeats
        self.prev_heartbeat_count = responses[2]
        self.heartbeat_count = responses[3]
        print("Heartbeat received, successful init!")

        # Wait until we receive request for data
        while (not self.signal_pin.read()):
            time.sleep(0.1)

        print("Received high on pin")
        print("Transmitting format message")
        # Transferring data format message
        self.spi.transfer(self.HEADERS["config"])
        time.sleep(1)

        self.spi.transfer(self.data_format_message)



if __name__ == "__main__":
    test = SPIComms(10)
    test.start_comms()

    while True:
        array = np.random.rand(10)
        #print(array)
        test.set_data(array)
        time.sleep(1.0/4000)