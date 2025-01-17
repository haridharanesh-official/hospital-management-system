import paho.mqtt.client as mqtt
import sqlite3
from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# MQTT Configuration
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_TOPIC = "hospital/waste_level"

# Email settings
EMAIL_SENDER = "yourhospital@gmail.com"
EMAIL_PASSWORD = "yourpassword"
CLEANING_STAFF_EMAIL = "cleaning@example.com"

# Function to send email alerts
def send_email_alert(alert_message):
    msg = MIMEText(alert_message)
    msg['From'] = EMAIL_SENDER
    msg['To'] = CLEANING_STAFF_EMAIL
    msg['Subject'] = "Waste Bin Alert"
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, CLEANING_STAFF_EMAIL, msg.as_string())
    server.quit()

# Initialize database
def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS waste_bins (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        location TEXT,
                        fill_level INTEGER,
                        last_updated TEXT)''')
    conn.commit()
    conn.close()

init_db()

# MQTT Callback function
def on_message(client, userdata, msg):
    try:
        data = msg.payload.decode("utf-8").split(',')
        location, fill_level = data[0], int(data[1])
        
        conn = sqlite3.connect("hospital.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO waste_bins (location, fill_level, last_updated) VALUES (?, ?, datetime('now'))", 
                       (location, fill_level))
        conn.commit()
        conn.close()
        
        if fill_level > 80:
            send_email_alert(f"Waste bin at {location} is over 80% full. Immediate action required!")
    except Exception as e:
        print("Error processing MQTT message:", e)

# Flask route to fetch waste bin data
@app.route("/waste_data", methods=["GET"])
def get_waste_data():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT location, fill_level, last_updated FROM waste_bins ORDER BY last_updated DESC")
    data = cursor.fetchall()
    conn.close()
    return jsonify(data)

# Web dashboard
@app.route("/")
def dashboard():
    return render_template("waste_dashboard.html")

# Start MQTT Client
def start_mqtt():
    client = mqtt.Client()
    client.on_message = on_message
    client.connect(MQTT_BROKER, 1883, 60)
    client.subscribe(MQTT_TOPIC)
    client.loop_start()

if __name__ == "__main__":
    start_mqtt()
    app.run(host="0.0.0.0", port=5007, debug=True)
