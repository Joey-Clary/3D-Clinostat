#include <ArduinoHttpClient.h>
#include <WiFiNINA.h>
#include <Arduino_LSM6DS3.h>
#include "arduino_secrets.h"

//Set Wifi credentials in arduino_secrets.h
//Wifi Settings
char ssid[] = SECRET_SSID; 
char pass[] = SECRET_PASS;

char serverAddress[] = "192.168.1.1"; //SET RECEIEVING COMPUTER IP ADDRESS
int port = 8080;

WiFiClient wifi;
WebSocketClient client = WebSocketClient(wifi, serverAddress, port);
int status = WL_IDLE_STATUS;

int failCount = 0;

unsigned long t;


void setup() {
  Serial.begin(9600);
  wifi_setup();
  
  //Setup for Accelerometer
  if (!IMU.begin()){
    Serial.println("Failed to initialize IMU!");
    while (1);
  }

  Serial.print("Accelerometer sample rate = ");
  Serial.print(IMU.accelerationSampleRate());
  Serial.println(" Hz");
  Serial.println();
  Serial.println("Acceleration in G's");
  Serial.println("X\tY\tZ");
}

void wifi_setup() {
  //Setup for WIFI
  while (status != WL_CONNECTED) {
    Serial.println(status);
    Serial.print("Attempting to connect to Network named: ");
    Serial.println(ssid);                   // print the network name (SSID);

    // Connect to WPA/WPA2 network:
    status = WiFi.begin(ssid, pass);
  }
  
  // print the SSID of the network you're attached to:
  Serial.print("SSID: ");
  Serial.println(WiFi.SSID());

  // print your WiFi shield's IP address:
  IPAddress ip = WiFi.localIP();
  Serial.print("IP Address: ");
  Serial.println(ip);
}

void loop() {
  float x,y,z;
  int messageSize;

  Serial.println("Starting WebSocket client");
  client.begin();
  Serial.println("Websocket Connected");

  while (client.connected()) {
    t = millis();
    if (IMU.accelerationAvailable()) {
      IMU.readAcceleration(x,y,z);
    
      client.beginMessage(TYPE_TEXT);
      client.print(x);
      client.print('\t');
      client.print(y);
      client.print('\t');
      client.print(z);
      client.print('\t');
      client.println(t);
      client.endMessage();

      Serial.print(x);
      Serial.print('\t');
      Serial.print(y);
      Serial.print('\t');
      Serial.println(z);
      messageSize = client.parseMessage();

      if (messageSize == 0) {
        failCount++;
        Serial.print("Fail: ");
        Serial.println(failCount);
      }
      else {
        failCount = 0;   
      }

      if (failCount > 10) {
        break;
      }
      
    }
    delay(1000);
  }
  client.stop();
  wifi_setup();
  client.println("disconnected\n");
  Serial.println("disconnected\n");
}
