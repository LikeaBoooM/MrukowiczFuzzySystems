#include "DHT.h"
#include <ArduinoJson.h>
#include <Arduino_JSON.h>
#include <WiFi.h>
#include <HTTPClient.h>
#define DHTTYPE DHT11   // DHT 11
#define DHTPIN 4
int led_red = 25;
int led_yellow = 26;
int led_green = 27;
const char* ssid = "MW40V_6256";
const char* password = "18828621";
String posturl = ""; 
//Your Domain name with URL path or IP address with path
const char* serverName = "http://192.168.1.197/";
const char* serverNametoOutput = "http://192.168.1.197/output/";
String sensorReadings;
float sensorReadingsArr[3];
// the following variables are unsigned longs because the time, measured in
// milliseconds, will quickly become a bigger number than can be stored in an int.
unsigned long lastTime = 0;
// Timer set to 10 minutes (600000)
//unsigned long timerDelay = 600000;
// Set timer to 5 seconds (5000)
unsigned long timerDelay = 5000;
DHT dht(DHTPIN, DHTTYPE);
int value = 20;
void setup() {

  pinMode(led_red, OUTPUT);
  pinMode(led_yellow, OUTPUT);
  pinMode(led_green, OUTPUT);
  
  digitalWrite(led_red, LOW);
  digitalWrite(led_yellow, LOW);
  digitalWrite(led_green, LOW);
  
  Serial.begin(115200);
  Serial.println(F("DHTxx test!"));
  dht.begin();
  WiFi.begin(ssid, password);
  Serial.println("Connecting");
  while(WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to WiFi network with IP Address: ");
  Serial.println(WiFi.localIP());
 
  Serial.println("Timer set to 5 seconds (timerDelay variable), it will take 5 seconds before publishing the first reading.");
}

void loop() {
  
  float outputValue = dataJSON();
  if (outputValue >= 0 && outputValue < 2.0){
       digitalWrite(led_red, HIGH);
       digitalWrite(led_yellow, LOW);
       digitalWrite(led_green, LOW);
  } else if (outputValue >= 2.0 && outputValue < 4.0){
       digitalWrite(led_red, HIGH);
       digitalWrite(led_yellow, HIGH);
       digitalWrite(led_green, LOW);
  } else if (outputValue >= 4.0 && outputValue < 6.0) {
       digitalWrite(led_yellow, HIGH);
       digitalWrite(led_red, LOW);
       digitalWrite(led_green, LOW);
  } else if (outputValue >= 6.0 && outputValue < 8.0) {
       digitalWrite(led_red, LOW);
       digitalWrite(led_yellow, HIGH);
       digitalWrite(led_green, HIGH);
  } else {
       digitalWrite(led_yellow, LOW);
       digitalWrite(led_red, LOW);
       digitalWrite(led_green, HIGH);
  }
  
  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float t = dht.readTemperature();
  // Read temperature as Fahrenheit (isFahrenheit = true)
  float f = dht.readTemperature(true);
  String humString = String(h);
  String temperatur = String(t);

  
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t) || isnan(f)) {
    Serial.println(F("Failed to read from DHT sensor!"));
    return;
  }

  // Compute heat index in Fahrenheit (the default)
  float hif = dht.computeHeatIndex(f, h);
  // Compute heat index in Celsius (isFahreheit = false)
  float hic = dht.computeHeatIndex(t, h, false);

  Serial.print(F("Humidity: "));
  Serial.print(h);
  Serial.print(F("%  Temperature: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print(f);
  Serial.print(F("°F  Heat index: "));
  Serial.print(hic);
  Serial.print(F("°C "));
  Serial.print(hif);
  Serial.println(F("°F"));

  Serial.println(outputValue);
  postJson(h, t, f);
  delay(2000);
}

void postJson(float hum, float temp, float oven){
      WiFiClient client;
      HTTPClient http;
      StaticJsonDocument<200> doc;
      serializeJson(doc, Serial);
      
      doc["humidity"] = hum ;
      doc["temeperature"] = temp ;
      doc["oventemperature"] = value;
      value++;

      if(value==50){
          value=20;
        }
      
      // Your Domain name with URL path or IP address with path
      http.begin(client, serverName);

      http.addHeader("Content-Type", "application/json");
      int httpResponseCode = http.POST(doc.as<String>());

      // If you need an HTTP request with a content type: text/plain
      //http.addHeader("Content-Type", "text/plain");
      //int httpResponseCode = http.POST("Hello, World!");
     
      Serial.print("HTTP Response code: ");
      Serial.println(httpResponseCode);
        
      // Free resources
      http.end();
    }

String httpGETRequest(const char* serverName) {
  WiFiClient client;
  HTTPClient http;
    
  // Your Domain name with URL path or IP address with path
  http.begin(client, serverName);
  
  // Send HTTP POST request
  int httpResponseCode = http.GET();
  
  String payload = "{}"; 
  
  if (httpResponseCode>0) {
    Serial.print("HTTP Response code: ");
    Serial.println(httpResponseCode);
    payload = http.getString();
  }
  else {
    Serial.print("Error code: ");
    Serial.println(httpResponseCode);
  }
  // Free resources
  http.end();

  return payload;
}

float dataJSON(){
      sensorReadings = httpGETRequest(serverNametoOutput);
      JSONVar myObject = JSON.parse(sensorReadings);
      
      if (JSON.typeof(myObject) == "undefined") {
        Serial.println("Parsing input failed!");
        return 0;
      }
      
      JSONVar keys = myObject.keys();
    
      for (int i = 0; i < keys.length(); i++) {
        JSONVar value = myObject[keys[i]];
        sensorReadingsArr[i] = double(value);
      }
      return sensorReadingsArr[1];
 }
