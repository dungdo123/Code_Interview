#include <Wire.h>
#include <LIDARLite.h>

LIDARLite myLidarLite;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);

  myLidarLite.begin(0, true);

  myLidarLite.configure(0);

}

void loop() {
  // put your main code here, to run repeatedly:
  Serial.println(myLidarLite.distance());

  for(int i = 0; i< 99; i++)
  {
    Serial.println(myLidarLite.distance(false));
    delay(0.1);
  }

}
