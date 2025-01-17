#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <Wire.h>
#include "MAX30100_PulseOximeter.h"
#include <DHT.h>

// WiFi credentials
const char* ssid = "hari_d_04";
const char* password = "harihari";

// Server details (Raspberry Pi Flask API)
const char* serverURL = "http://192.168.43.117:5000/api/sensor-data"; 

// Define DHT sensor type and pin
#define DHTPIN D2
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);

// Initialize pulse oximeter
PulseOximeter pox;
#define REPORTING_PERIOD_MS 1000
uint32_t tsLastReport = 0;

// Sensor data variables
float temperature;
float humidity;
float heartRate = 0;
float spo2 = 0;

void onBeatDetected() {
    Serial.println("Beat detected!");
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);
    
    // Connect to WiFi
    Serial.print("Connecting to WiFi...");
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("\nConnected to WiFi");

    // Initialize sensors
    dht.begin();
    
    if (!pox.begin()) {
        Serial.println("MAX30100 init failed");
        while (1);
    }
    pox.setOnBeatDetectedCallback(onBeatDetected);
}

void loop() {
    // Update pulse oximeter readings
    pox.update();
    
    // Read sensor values
    temperature = dht.readTemperature();
    humidity = dht.readHumidity();
    
    if (millis() - tsLastReport > REPORTING_PERIOD_MS) {
        heartRate = pox.getHeartRate();
        spo2 = pox.getSpO2();
        
        Serial.print("Heart Rate: "); Serial.println(heartRate);
        Serial.print("SpO2: "); Serial.println(spo2);
        Serial.print("Temperature: "); Serial.println(temperature);
        Serial.print("Humidity: "); Serial.println(humidity);
        
        // Send data to Raspberry Pi backend
        sendSensorData(temperature, humidity, heartRate, spo2);
        
        tsLastReport = millis();
    }
}

// Function to send data to the Raspberry Pi backend
void sendSensorData(float temp, float hum, float hr, float sp) {
    if (WiFi.status() == WL_CONNECTED) {
        HTTPClient http;
        http.begin(serverURL);
        http.addHeader("Content-Type", "application/json");

        String payload = "{\"temperature\":" + String(temp) +
                         ", \"humidity\":" + String(hum) +
                         ", \"heart_rate\":" + String(hr) +
                         ", \"spo2\":" + String(sp) + "}";

        int httpResponseCode = http.POST(payload);
        
        Serial.print("HTTP Response code: ");
        Serial.println(httpResponseCode);
        
        http.end();
    } else {
        Serial.println("WiFi not connected");
    }
}
