# Posenet Data API
This document describes the format of the Posenet data streamed from the Anything Sensor to the Arduino. Posenet is a neural net that tracks human poses in an image. 

## Posenet Data

When Posenet is running inference, it outputs a Pose object for each person it has detected in the frame. Each Pose object contains 17 Keypoints that represent the pose coordinates of various parts of the body. Each Keypoint contains (x,y) coordinates and a confidence score, which describes how confident the neural net is that it has found that keypoint. The confidence score can be used to filter out any Keypoints that may not be accurate. Here is a list of all Keypoints that are tracked:

Keypoint: (x, y, confidence_score)

0: Nose  
1: Left Eye  
2: Right Eye  
3: Left Ear  
4: Right Ear  
5: Left Shoulder  
6: Right Shoulder  
7: Left Elbow  
8: Right Elbow  
9: Left Wrist  
10: Right Wrist  
11: Left Hip  
12: Right Hip  
13: Left Knee  
14: Right Knee  
15: Left Ankle  
16: Right Ankle  

## Arduino API

The Keypoints are sent to the Arduino as a 1-D array. The keypoints are sent as (x, y, confidence_score) in the order listed above. So for example, this would be the code to access the three elements of the "Right Elbow" keypoint:


```
# include "AnythingSensor.h"
AnythingSensor sensor = AnythingSensor();

void setup() {
    Serial.begin (9600);
    sensor.begin();
}

void loop() {
    sensor.read();

    // Right Elbow index
    int index = 8;

    // x-coordinate
    Serial.println(sensor.get(index * 3));

    // y-coordinate
    Serial.println(sensor.get(index * 3 + 1));

    // confidence score
    Serial.println(sensor.get(index * 3 + 2));
    
}
```