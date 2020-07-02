# Face Detection Data API
This document describes the format of the face detection data streamed from the Anything Sensor to the Arduino. 

## Face detection Data

The face detection neural net outputs the x and y-coordinates for 2 faces in the image. If there is only one face, then the (0, 0) is output for the second face.

## Arduino API

The two face coordinates are sent to the Arduino as a 1-D array with 4 elements:

`[x1, y1, x2, y2]`

For example, to read the coordinates of the second face:

```
# include "AnythingSensor.h"
AnythingSensor sensor = AnythingSensor();

void setup() {
    Serial.begin (9600);
    sensor.begin();
}

void loop() {
    sensor.read();

    // Face index
    int index = 1;

    // x-coordinate
    Serial.println(sensor.get(index * 2));

    // y-coordinate
    Serial.println(sensor.get(index * 2 + 1));

}
```