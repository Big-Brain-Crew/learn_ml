# SPI Communication Protocol
This document describes the protocol that the microcontroller and Coral expect to communicate data over SPI. Currently, the devices are configured such that the Coral is the master and the microcontroller is the slave.

## SPI Settings

* Max Speed: 10 kHz
* Bits per word: 8
* Bit order: MSB
* SPI Mode: 0

## Wiring
This protocol uses the standard 4-wire SPI protocol with an GPIO wire and ground wire. This is a total of 6 wires. The GPIO pin should be configured as an output on the microcontroller and as an input on the Coral.

### Arduino Wiring
The Arduino library requires the following wiring:

| Name          | Arduino Pin      | Coral Pin      |
| :---:         | :---:            | :---:          |
| GND           | GND              | GND (14)       |
| SCK           | 13               | 23             |
| MISO          | 12               | 21             |
| MOSI          | 11               | 19             |
| SS            | 10               | 24             |
| SIGNAL (GPIO) | 9                | 13             |

## Message Format
Each message contains 2 parts: the header and the message body.

### Header
The header is a 1 byte message. It describes what content will be contained in the body. The current valid headers are listed below in the table below.

| Header Value          | Meaning      | Message Body Length |
| :---:                 | :---:        | :---:               |
| 0x10                  | Hearbeat     | 0 bytes             |
| 0x20                  | Config       | 4 bytes             |
| 0x30                  | Data         | Data length         |

The data length is variable determined by the output size of the neural net. This data length size is specified in a config message and then cannot be changed afterwards.

### Body
The body of the message is a series of bytes of the length determined by the header. The messages are in MSB format.

## Initialization sequence
### Coral
1. While waiting for a connection from the microcontroller, the Coral should be sending 0XFF constantly on the SPI channel. The microcontroller should respond with a series of three bytes: 0xFF, 0xFE, 0xFD (in that sequence).
2. Next, a config message must be sent over SPI. First, the config header is transferred, followed by an empty message [0x00,0x00,0x00,0x00] to signal to the microcontroller that the Coral successfully received the heartbeat.
3. After that message is transferred, the Coral should wait for a HIGH on the signal pin, signifying the Arduino is ready to receive the config
4. Once the high is received, the config message should be sent. Send the config header, followed by the following 4 bytes:

| Position              | Value        |  Info                     |
| :---:                 | :---:        |  :---:                    |
| 0                     | Datatype     | Currently not implemented |
| 1                     | Data Length  | Length of data in bytes   |
| 2                     | Empty        | Value can be anything     |
| 3                     | Empty        | Value can be anything     |

### Microcontroller
1. Listen for messages sent via SPI. After received one 0xFF, load 0xFF into buffer to send to the Coral. This value should be decremented every time a transfer occurs, until a total of 4 0xFF messages are received.
2. Listen for a config header followed by a message body containing [0x00, 0x00, 0x00, 0x00]. This is an acknowledgement by the Coral that it received the response correctly.
3. Once the microcontroller is ready to receive the config information, raise the SIGNAL line high.
4. Listen for the config and configure the buffer and message fields correctly. The message format is listed above.


## Heartbeat
The coral should send a heartbeat at a regular frequency to the microcontroller to check availability. The response from the microcontroller should increment on every message transferred (including non-heartbeat messages), except where there is an overflow (0xFF -> 0x00). If the heartbeat message is no longer incrementing, the microcontroller is unavailable or has been reset. The communications should return to init state.