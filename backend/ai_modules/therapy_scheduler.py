from flask import Flask, request, jsonify, render_template
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
import datetime
import threading

app = Flask(__name__)

EMAIL_SENDER = "yourhospital@gmail.com"
EMAIL_PASSWORD = "yourpassword"
TWILIO_SID = "your_twilio_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE = "your_twilio_phone_number"
DOCTOR_EMAILS = ["doctor1@example.com", "doctor2@example.com"]
NURSE_EMAILS = ["nurse1@example.com", "nurse2@example.com"]

# Database Initialization
def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS therapy_schedule (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id INTEGER,
                        therapy TEXT,
                        scheduled_time TEXT,
                        adjusted_time TEXT,
                        doctor_override TEXT,
                        status TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Send Email Notifications
def send_email(subject, body, recipients):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, recipients, msg.as_string())
    server.quit()

# Send SMS Notifications
def send_sms(body, recipients):
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    for recipient in recipients:
        client.messages.create(
            body=body,
            from_=TWILIO_PHONE,
            to=recipient
        )

# API to Add Therapy Session (AI Suggested)
@app.route("/add_therapy", methods=["POST"])
def add_therapy():
    data = request.json
    patient_id = data.get("patient_id")
    therapy = data.get("therapy")
    scheduled_time = data.get("scheduled_time")
    
    if not all([patient_id, therapy, scheduled_time]):
        return jsonify({"error": "All fields are required"}), 400
    
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO therapy_schedule (patient_id, therapy, scheduled_time, status) VALUES (?, ?, ?, ?)",
                   (patient_id, therapy, scheduled_time, "Scheduled"))
    conn.commit()
    conn.close()
    
    email_subject = "New Therapy Session Assigned"
    email_body = f"A new therapy session for Patient {patient_id} has been scheduled at {scheduled_time}."
    send_email(email_subject, email_body, DOCTOR_EMAILS + NURSE_EMAILS)
    send_sms(email_body, ["+1234567890", "+0987654321"])  # Replace with actual numbers
    
    return jsonify({"message": "Therapy session added and notifications sent"})

# API for Doctor Override
@app.route("/override_therapy", methods=["POST"])
def override_therapy():
    data = request.json
    therapy_id = data.get("therapy_id")
    adjusted_time = data.get("adjusted_time")
    doctor_name = data.get("doctor_name")
    
    if not all([therapy_id, adjusted_time, doctor_name]):
        return jsonify({"error": "All fields are required"}), 400
    
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE therapy_schedule SET adjusted_time = ?, doctor_override = ?, status = ? WHERE id = ?",
                   (adjusted_time, doctor_name, "Rescheduled", therapy_id))
    conn.commit()
    conn.close()
    
    email_subject = "Therapy Session Rescheduled"
    email_body = f"Doctor {doctor_name} has rescheduled Therapy Session {therapy_id} to {adjusted_time}."
    send_email(email_subject, email_body, DOCTOR_EMAILS + NURSE_EMAILS)
    send_sms(email_body, ["+1234567890", "+0987654321"])  # Replace with actual numbers
    
    return jsonify({"message": "Therapy session rescheduled and notifications sent"})

# API to Generate Therapy Report
@app.route("/generate_report", methods=["GET"])
def generate_report():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM therapy_schedule")
    records = cursor.fetchall()
    conn.close()
    
    report = "Therapy Report:\n" + "\n".join([str(record) for record in records])
    email_subject = "Monthly Therapy Report"
    send_email(email_subject, report, DOCTOR_EMAILS)
    
    return jsonify({"message": "Therapy report generated and emailed to doctors"})

# Real-Time Dashboard UI
@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM therapy_schedule")
    records = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", therapy_data=records)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)
