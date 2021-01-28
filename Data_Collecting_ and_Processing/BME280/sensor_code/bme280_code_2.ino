#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <LowPower.h>

#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME280 bme; // I2C

unsigned long delayTime;
float buf[3];

void setup() {
  // put your setup code here, to run once:
    Serial.begin(9600);
    while(!Serial);    // time to get serial running
    //Serial.println(F("BME280 test"));

    unsigned status;
    status = bme.begin();

    if(!status){
      Serial.println("could not connect");
      while (1);
    }
   //Serial.println("-- Default Test --");
    delayTime = 10000;

    Serial.println();
}

void loop() {
  // put your main code here, to run repeatedly:
    
  
   
    printValues();
    delay(delayTime);
}
void printValues(){
  buf[0] = bme.readTemperature();
  buf[1] = bme.readHumidity();
  buf[2] = bme.readPressure()/100.0F;
  for (int i=0;i<3;i++){
    Serial.print(buf[i]);  
    Serial.print(" ");
    }
    Serial.print("\n");
}
