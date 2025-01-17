import time
import Adafruit_DHT
import RPi.GPIO as GPIO
from flask import Flask, jsonify

app = Flask(__name__)

# Sensor configurations
DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
LDR_PIN = 17

def read_temperature_humidity():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    if humidity is not None and temperature is not None:
        return {"temperature": temperature, "humidity": humidity}
    else:
        return {"error": "Failed to retrieve data"}

def read_light_intensity():
    GPIO.setup(LDR_PIN, GPIO.IN)
    return {"light_intensity": GPIO.input(LDR_PIN)}

@app.route("/rpi_sensors", methods=["GET"])
def get_sensor_data():
    return jsonify({
        "temperature_humidity": read_temperature_humidity(),
        "light_intensity": read_light_intensity()
    })

if __name__ == "__main__":
    GPIO.setmode(GPIO.BCM)
    try:
        app.run(host="0.0.0.0", port=5004, debug=True)
    finally:
        GPIO.cleanup()
