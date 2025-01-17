from flask import Flask, request, jsonify
import sqlite3
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)

EMAIL_SENDER = "yourhospital@gmail.com"
EMAIL_PASSWORD = "yourpassword"
STAFF_EMAILS = [
    "staff1@example.com",
    "staff2@example.com",
    "staff3@example.com",
    "staff4@example.com",
    "staff5@example.com"
]

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

# Initialize database
def init_db():
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS staff (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        role TEXT,
                        shift TEXT,
                        contact TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS shifts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        staff_id INTEGER,
                        date TEXT,
                        start_time TEXT,
                        end_time TEXT,
                        FOREIGN KEY(staff_id) REFERENCES staff(id))''')
    conn.commit()
    conn.close()

init_db()

# Add shift schedule with notification
@app.route("/add_shift", methods=["POST"])
def add_shift():
    data = request.json
    staff_id = data.get("staff_id")
    date = data.get("date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    
    if not all([staff_id, date, start_time, end_time]):
        return jsonify({"error": "All fields are required"}), 400
    
    conn = sqlite3.connect("hospital.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM staff WHERE id = ?", (staff_id,))
    staff_name = cursor.fetchone()
    
    if not staff_name:
        return jsonify({"error": "Staff not found"}), 400
    
    cursor.execute("INSERT INTO shifts (staff_id, date, start_time, end_time) VALUES (?, ?, ?, ?)",
                   (staff_id, date, start_time, end_time))
    conn.commit()
    conn.close()
    
    email_subject = "New Shift Assigned"
    email_body = f"Dear {staff_name[0]},\n\nYou have been assigned a new shift on {date} from {start_time} to {end_time}.\n\nBest Regards,\nHospital Management"
    send_email(email_subject, email_body, STAFF_EMAILS)
    
    return jsonify({"message": "Shift added successfully, notification sent"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=True)
