#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <string.h>
#include <LiquidCrystal_I2C.h>
#include <Wire.h>

LiquidCrystal_I2C lcd(0x27,16,2);



const char WIFI_SSID[] = "Anhkhanh";
const char WIFI_PSK[] = "anhkhanh91";

const char http_site[] = "alohahaha.tk";
const int http_port = 80;

int id ;
String id_string;

//Pin definitions
const int LED_PIN = 5;

//Global variables
WiFiClient client;

LiquidCrystal_I2C lcd(0x27,16,4);

void setup(){
  
  // id= ESP.getChipId();
   id=1;
   id_string = String(id);
   Wire.begin(13,12);
   lcd.begin();
   lcd.backlight();
  
   

   pinMode(LED_PIN,OUTPUT);
  
   connectWifi();
  
   if(!getPage()){
     lcd.setCursor(0,0);
     lcd.print("not connect");
  }
}

void loop(){
  //if there are incoming bytes,print them
  if(client.available()){
    char c = client.read();
      Serial.print(c); 
  }
 
  if(!client.connected()){
   
    //close socket and wait for disconect from Wifi
    client.stop();
    if(WiFi.status() != WL_DISCONNECTED){
      WiFi.disconnect();
      delay(10000);
    }
    //Turn off LED
    digitalWrite(LED_PIN,LOW);
    //Do nothing
    
    while(true){
      delay(1000);
    } 
  }
}

//Attempt tp connect to Wifi
void connectWifi(){
  byte led_status = 0;
  
  WiFi.mode(WIFI_STA);
 
  WiFi.begin(WIFI_SSID,WIFI_PSK);
  
  while (WiFi.status() != WL_CONNECTED){
    digitalWrite(LED_PIN,led_status);
    led_status ^= 0x01;
    delay(100);
  }
  
  digitalWrite(LED_PIN,HIGH);
}

//perform an HTTP GET request to a remote page
bool getPage(){
  //Attempt to make a connection to the remote server
  if(!client.connect(http_site,http_port)){
    return false;
  }
  //make an HTTP GET request
  client.print("GET /get.php?id=");
  client.print(id_string);
  client.println(" HTTP/1.1");
  client.print("Host: ");
  client.println(http_site);
  client.println("Connection: close");
  client.println();

  return true;
}










