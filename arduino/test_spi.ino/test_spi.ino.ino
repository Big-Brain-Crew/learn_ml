#include "pins_arduino.h"
#include "AnythingSensor.h"


AnythingSensor sensor = AnythingSensor();

void setup()
{
 Serial.begin (9600);   // debugging
 Serial.println("Beginning comms");

 
 sensor.begin();

}  

// main loop - wait for flag set in interrupt routine
void loop (void)
{
  sensor.read();

  for(int i = 0; i < sensor.length(); i++)
  {
    Serial.print(sensor.get(i));
    Serial.print(" ");
  }
  Serial.println(" ");
  delay(10);
//   
}  // end of loop
