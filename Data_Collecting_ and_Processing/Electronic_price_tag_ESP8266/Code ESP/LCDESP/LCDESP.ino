
#include <LiquidCrystal_I2C.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <Wire.h>

const char WIFI_SSID[] = "FPT Telecom";
const char WIFI_PSK[] = "bkfet1234";

const char http_site[] = "trananh-test.tk";
const int http_port = 80;

int id ;
String id_string;
char gia[16];
char tensp[16];
char a=0,b=0,d=0,i,j,k,l,m;

WiFiClient client;
LiquidCrystal_I2C lcd(0x3F,16,2);

void setup(){
  
   id= ESP.getChipId();
   //id=2;
   id_string = String(id);
   Wire.begin(13,12);
   lcd.begin();
   lcd.backlight();
   connectWifi();
 
}

void loop(){
  if (a==0){
      getPage();
      a=1;
      j=0;
      m=0;
      }
      
  if(client.available()){
    
    char c = client.read();
    if (d == 1)    d=2;
    if (b == 1)    b=2;
    if (c =='[')   b=1;
    if (c ==']')   b=0;
    if (c == '{')  d=1;
    if (c == '}')  d=0;
    if(b==2){
      gia[j] = c;
      j++;
    }
    if(d==2){
      tensp[m] = c;
      m++;
    }
    }
  if(!client.connected()){
    lcd.clear();
    lcd.setCursor(0,0);
    lcd.print("name:");
    lcd.print(tensp); 
    lcd.setCursor(0,1);
    lcd.print("cost:");
    lcd.print(gia);
    client.stop();
    delay(15000);
    a=0;
    for (i=0;i<j;i++){
      gia[i]=' '; 
    }
    for (l=0;l<m;l++){
      tensp[l]=' ';
    }
  }
  
}

//Attempt tp connect to Wifi
void connectWifi(){
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID,WIFI_PSK);
  while (WiFi.status() != WL_CONNECTED){
    k++;
    lcd.print(".");
    delay(1000);
    if(k>15) {
      lcd.clear();
      lcd.print("not connected");
      delay(3000);
      ESP.reset();
    } 
  }
}


void getPage(){
  if(!client.connect(http_site,http_port)){
      lcd.print("web fail");
      delay(3000);
      ESP.reset();
  }
  client.print("GET /get.php?id=");
  client.print(id_string);
  client.println(" HTTP/1.1");
  client.print("Host: ");
  client.println(http_site);
  client.println("Connection: close");
  client.println();
}











