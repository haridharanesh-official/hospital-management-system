from flask import Flask, request, jsonify, render_template
import sqlite3
import smtplib
from email.mime.text import MIMEText
import requests

app = Flask(__name__)

# Email settings
EMAIL_SENDER = "yourhospital@gmail.com"
EMAIL_PASSWORD = "yourpassword"
ALERT_EMAIL = "doctor@example.com"

ESP8266_API_URL = "http://esp8266-device.local/data"  # Replace with actual ESP8266 URL
HOSPITAL_AI_API = "http://hospital-ai.local/analyze"  # Replace with actual Hospital AI URL

# Initialize database
def init_db():
    conn = sqlite3.connect("medication.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        age INTEGER,
                        condition TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS medications (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER,
                        medication TEXT,
                        dosage TEXT,
                        schedule TEXT,
                        doctor_override TEXT,
                        refill_needed INTEGER DEFAULT 0,
                        FOREIGN KEY(patient_id) REFERENCES patients(id))''')
    conn.commit()
    conn.close()

init_db()

# Function to send email alerts
def send_email_alert(patient_name, medication, reason):
    msg = MIMEText(f"Alert: {patient_name} has a medication issue: {reason} for {medication}.")
    msg['From'] = EMAIL_SENDER
    msg['To'] = ALERT_EMAIL
    msg['Subject'] = "Medication Alert"
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, ALERT_EMAIL, msg.as_string())
    server.quit()

# Function to fetch patient vitals from ESP8266
def get_patient_vitals():
    try:
        response = requests.get(ESP8266_API_URL)
        return response.json()
    except Exception as e:
        print(f"Error fetching vitals: {e}")
        return {}

# Function to send data to Hospital AI
def analyze_vitals_with_ai(patient_id, vitals):
    try:
        response = requests.post(HOSPITAL_AI_API, json={"patient_id": patient_id, "vitals": vitals})
        return response.json()
    except Exception as e:
        print(f"Error communicating with AI: {e}")
        return {}

# API to add medication schedule
@app.route("/add_medication", methods=["POST"])
def add_medication():
    data = request.json
    patient_id = data.get("patient_id")
    medication = data.get("medication")
    dosage = data.get("dosage")
    schedule = data.get("schedule")
    doctor_override = data.get("doctor_override", "No")
    refill_needed = data.get("refill_needed", 0)
    
    if not all([patient_id, medication, dosage, schedule]):
        return jsonify({"error": "All fields are required"}), 400
    
    conn = sqlite3.connect("medication.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO medications (patient_id, medication, dosage, schedule, doctor_override, refill_needed) VALUES (?, ?, ?, ?, ?, ?)",
                   (patient_id, medication, dosage, schedule, doctor_override, refill_needed))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Medication added successfully"})

# API to check for medication refill reminders
@app.route("/check_refills", methods=["GET"])
def check_refills():
    conn = sqlite3.connect("medication.db")
    cursor = conn.cursor()
    cursor.execute("SELECT patients.name, medications.medication FROM medications JOIN patients ON patients.id = medications.patient_id WHERE refill_needed = 1")
    refills = cursor.fetchall()
    conn.close()
    
    for patient_name, medication in refills:
        send_email_alert(patient_name, medication, "Medication refill needed")
    
    return jsonify({"message": "Refill alerts sent where necessary"})

# API to get medication details
@app.route("/get_medications/<int:patient_id>", methods=["GET"])
def get_medications(patient_id):
    conn = sqlite3.connect("medication.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medications WHERE patient_id = ?", (patient_id,))
    medications = cursor.fetchall()
    conn.close()
    return jsonify({"medications": medications})

# Web UI for viewing patient medication
@app.route("/")
def dashboard():
    conn = sqlite3.connect("medication.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM medications")
    medications = cursor.fetchall()
    conn.close()
    return render_template("medication_dashboard.html", medications=medications)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
