#include <LiquidCrystal_I2C.h>

#include <Wire.h>

LiquidCrystal_I2C lcd(0x27,16,4);


void setup() {
   Wire.begin(13,12);
   lcd.begin();
   lcd.backlight();
   lcd.setCursor(0,0);
   lcd.print("chao a dung");
}
void loop() {
  // put your main code here, to run repeatedly:

}
