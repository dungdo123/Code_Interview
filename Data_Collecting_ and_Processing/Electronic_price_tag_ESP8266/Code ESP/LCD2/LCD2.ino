
#include <LiquidCrystal_I2C.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <string.h>
#include <Wire.h>

const char WIFI_SSID[] = "BKAT";
const char WIFI_PSK[] = "12345678";

const char http_site[] = "alohahaha.tk";
const int http_port = 80;
const int sleepTimeS = 10;
int id ;
String id_string;
char linhkien[10];
char gia[10];
char a=0,b=0,i=0,j=0;
//Pin definitions
const int LED_PIN = 5;

//Global variables
WiFiClient client;
LiquidCrystal_I2C lcd(0x27,16,2);
void setup(){
  
   //id= ESP.getChipId();
   id=1;
   id_string = String(id);
   Wire.begin(13,12);
   lcd.begin();
   lcd.backlight();
   lcd.clear();
   lcd.print("ID:");
   lcd.print(id_string);  
   pinMode(LED_PIN,OUTPUT);  
   connectWifi();
  
   if(!getPage()){
     lcd.setCursor(0,0);
     lcd.print("web fail");
  }
}

void loop(){
  //if there are incoming bytes,print them
  if(client.available()){
    char c = client.read();
    if (a==1)    a=2;
    if (b==1)    b=2;
    if (c=='{')  a=1;
    if (c=='}')  a=0;
    if (c=='[')  b=1;
    if (c==']')  b=0;
    if(a==2){
      linhkien[i]=c;
      i++;
    }
    if(b==2){
      gia[j] = c;
      j++;
    }
    }
  if(!client.connected()){
   
    //close socket and wait for disconect from Wifi
    lcd.setCursor(0,0);
    lcd.print(linhkien);
    lcd.setCursor(0,1);
    lcd.print(gia); 
    client.stop();
    ESP.deepSleep(sleepTimeS*1000);
    ESP.reset(); 
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










