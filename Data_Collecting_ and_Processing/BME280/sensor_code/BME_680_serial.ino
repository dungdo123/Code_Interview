

#include <Wire.h>


#include "Adafruit_BME680.h"
#define SEALEVELPRESSURE_HPA (1013.25)

Adafruit_BME680 bme; //i2c

float humidity = 0.25;
float gas = 0.75;

int humidity_score, gas_score;
float gas_reference = 2500; // do not understand
float hum_reference = 40;
int getgasreference_count = 0;
int gas_lower_limit = 10000; //bad air quality
int gas_upper_limit = 30000; //good air quality
unsigned long delayTime;
float buf[3];

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Wire.begin();
  if (!bme.begin()){
    Serial.println("Could not find a valid BME680 sensor, check wiring!");
    while(1);
  }
  else 
   bme.setTemperatureOversampling(BME680_OS_8X);
   bme.setHumidityOversampling(BME680_OS_2X);
   bme.setPressureOversampling(BME680_OS_4X);
   bme.setIIRFilterSize(BME680_FILTER_SIZE_3);
   delayTime = 500;
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
  buf[2] = bme.readPressure();

  for (int i=0; i<3; i++){
    Serial.print(buf[i]);
    Serial.print(" ");
  }
  Serial.print("\n");
}
