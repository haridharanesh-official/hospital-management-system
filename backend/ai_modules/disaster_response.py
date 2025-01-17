import requests
import sqlite3
import smtplib
import paho.mqtt.client as mqtt
from email.mime.text import MIMEText
from flask import Flask, jsonify

app = Flask(__name__)

# OpenWeatherMap API (Replace 'your_api_key' with an actual API key)
WEATHER_API_KEY = "eff14a855dfbb00570eb14b9d2357054"
WEATHER_CITY = "Tirupur"
WEATHER_URL = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric"

# MQTT settings for IoT sensor integration
MQTT_BROKER = "your_mqtt_broker"
MQTT_TOPIC = "hospital/disaster"

# Email settings
EMAIL_SENDER = "haridharanesh.sp@gmail.com"
EMAIL_PASSWORD = "hari041007"
DISASTER_TEAM_EMAILS = ["disaster1@example.com", "disaster2@example.com"]

# Function to send alerts
def send_email_alert(subject, message):
    msg = MIMEText(message)
    msg['From'] = EMAIL_SENDER
    msg['To'] = ", ".join(DISASTER_TEAM_EMAILS)
    msg['Subject'] = subject
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, DISASTER_TEAM_EMAILS, msg.as_string())
    server.quit()

# Initialize database
def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS disaster_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event TEXT,
                        severity TEXT,
                        source TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

init_db()

# Fetch weather updates
@app.route("/weather_alert", methods=["GET"])
def get_weather_alert():
    response = requests.get(WEATHER_URL)
    weather_data = response.json()
    
    if weather_data["cod"] == 200:
        weather_main = weather_data["weather"][0]["main"]
        temp = weather_data["main"]["temp"]
        
        if weather_main in ["Thunderstorm", "Rain", "Extreme"]:
            alert_message = f"Severe weather alert: {weather_main} with temperature {temp}°C. Take precautions!"
            send_email_alert("Severe Weather Alert", alert_message)
            
            conn = sqlite3.connect("hospital.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO disaster_logs (event, severity, source) VALUES (?, ?, ?)", (weather_main, "High", "Weather API"))
            conn.commit()
            conn.close()
            
        return jsonify({"status": "Weather alert checked", "weather": weather_main, "temperature": temp})
    else:
        return jsonify({"error": "Unable to fetch weather data"}), 500

# MQTT callback function
def on_message(client, userdata, msg):
    sensor_data = msg.payload.decode("utf-8")
    alert_message = f"IoT Sensor Alert: {sensor_data}. Immediate attention required!"
    send_email_alert("IoT Sensor Alert", alert_message)
    
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO disaster_logs (event, severity, source) VALUES (?, ?, ?)", (sensor_data, "High", "IoT Sensor"))
    conn.commit()
    conn.close()

# MQTT client setup
client = mqtt.Client()
client.on_message = on_message
client.connect(MQTT_BROKER, 1883, 60)
client.subscribe(MQTT_TOPIC)
client.loop_start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5008, debug=True)
