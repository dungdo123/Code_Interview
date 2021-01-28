#include <ESP8266WiFi.h>

const char *ssid = "ESPap";

WiFiServer server(80);

void setup() {
   delay(1000);
   Serial.begin(115200);
   Serial.println();
   Serial.print("Configuring access point...");

   WiFi.softAP(ssid);

   while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }

   Serial.println("done");
   IPAddress myIP = WiFi.softAPIP();
   Serial.print("AP IP address: ");
   Serial.println(myIP);

   server.begin();
   Serial.println("HTTP server started");
}

void loop() {

}
