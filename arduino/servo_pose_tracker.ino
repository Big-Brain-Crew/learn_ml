/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>
#include <AnythingSensor.h>

Servo myservo;  // create servo object to control a servo
AnythingSensor sensor = AnythingSensor();

int pos = 0;    // variable to store the servo position
int CONFIDENCE_THRESHOLD = 0.1;
int IMAGE_WIDTH = 640;
float SERVO_SCALE = 3.56;

void setup() {
  Serial.begin (9600);   // debugging
  Serial.println("Beginning comms");
  
  myservo.attach(6);  // attaches the servo on pin 9 to the servo object
  sensor.begin();
}

int servo_pos = 0;
void loop() {

  sensor.read();


//  int servo_pos = 0;
  if (sensor.get(2) > CONFIDENCE_THRESHOLD) {
    myservo.write(round(sensor.get(0) / SERVO_SCALE));
//    Serial.println(sensor.get(0));
//    Serial.println(sensor.get(1));
//    Serial.println(round(sensor.get(0) / 3.56));
  }
  
  
//  for(int i = 0; i < sensor.length(); i++)
//  {
//    Serial.print(sensor.get(i));
//    Serial.print(" ");
//  }
//  Serial.println(" ");
  delay(10);
  
//  for (pos = 0; pos <= 180; pos += 1) { // goes from 0 degrees to 180 degrees
//    // in steps of 1 degree
//    myservo.write(pos);              // tell servo to go to position in variable 'pos'
//    delay(15);                       // waits 15ms for the servo to reach the position
//  }
//  for (pos = 180; pos >= 0; pos -= 1) { // goes from 180 degrees to 0 degrees
//    myservo.write(pos);              // tell servo to go to position in variable 'pos'
//    delay(15);                       // waits 15ms for the servo to reach the position
//  }
}
