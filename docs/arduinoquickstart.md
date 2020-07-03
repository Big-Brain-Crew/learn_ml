# Arduino Quickstart

This guide will explain how to use the Anything Sensor for an Arduino project, including wiring the sensor, configuring the library in the Arduino IDE, and reading from the sensor in the sketch.

## Wiring the Anything Sensor
To connect the Anything Sensor to the Arduino, you will need to use the 6-pin connector included in the packaging. Plug the 6 pin connector into the port on the Anything Sensor as shown in the image below. On the Arduino, the 6 pins will connect to **pins 9-14** on the Arduino (14 is a ground pin).


  **The BLACK wire connects to the ground pin**

The connection on the Arduino should look like the picture below, make sure yours look likes this before you power the Arduino or Anything Sensor on.

## Configuring the Anything Sensor library in the Arduino IDE
Download the library zip file, available [here](https://google.com). Launch the Arduino IDE and go to Sketch --> Include Library --> Add .ZIP Library. Select the library zip file you downloaded earlier.

To test your installation, add the following line to the top of your Arduino sketch.

```
#include <AnythingSensor.h>
```

If your sketch compiles, you have correctly installed the library.

## Using the Anything Sensor in your Sketch
First, as we did above, you must include the Anything Sensor library in your sketch.

```
#include <AnythingSensor.h>
```

After you include statements, you need to create an AnythingSensor object, which you will use to read data from the sensor. You should do this above your setup function, where you define all of your other variables.

```
AnythingSensor sensor = AnythingSensor();
```

Next, you need to initialize and start communicating with the sensor. To do this, you use the `begin()` function. You should call this function in your setup function. NOTE: The program will wait at the `begin` function until the AnythingSensor is connected and turned on (and the program is started).

```
sensor.begin();
```

There are two functions to get data from the Anything Sensor. The first, `read()` will read the data from the Anything Sensor and store it on the Arduino. However, it will not give you any of the data. You can use the `get` function to access data. Additionally, there is a `length()` function that will return how many data points the sensor is sending to the Arduino. Here is an example loop function that will print all of the data the Anything Sensor sends.
```
void loop()
{
  // Read the most reent data from the sensor
  sensor.read();

  // Loop over all data from the sensor
  for(int i = 0; i < sensor.length(); i++)
  {
    // Use the get function to read the data
    Serial.print(sensor.get(i));
    Serial.print(" ");
  }
  Serial.println(" ");


  delay(10);
}
```

The `get()` function expects an index (int) specifying which data point to retrieve and will always return a float.

Here is the whole program together:
```
#include <AnythingSensor.h>

AnythingSensor sensor = AnythingSensor();

void setup()
{
 // Start the serial terminal
 Serial.begin(9600);
 Serial.println("Starting program");

 // Initialize the sensor
 sensor.begin();
}

void loop()
{
  // Read the most reent data from the sensor
  sensor.read();

  // Loop over all data from the sensor
  for(int i = 0; i < sensor.length(); i++)
  {
    // Use the get function to read the data
    Serial.print(sensor.get(i));
    Serial.print(" ");
  }
  Serial.println(" ");

  delay(10);
}
```
