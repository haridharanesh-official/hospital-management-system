import cv2
import sqlite3
import smtplib
from deepface import DeepFace
from flask import Flask, jsonify, render_template
from email.mime.text import MIMEText

app = Flask(__name__)

# Email settings
EMAIL_SENDER = "haridharanesh.sp@gmail.com"
EMAIL_PASSWORD = "hari041007"
ALERT_EMAIL = "ak6811182@gmail.com"

# Initialize database
def init_db():
    conn = sqlite3.connect("emotion_logs.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS emotions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        emotion TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Function to send email alerts
def send_email_alert(patient_id, emotion):
    msg = MIMEText(f"Patient {patient_id} has been experiencing prolonged negative emotions: {emotion}.")
    msg['From'] = EMAIL_SENDER
    msg['To'] = ALERT_EMAIL
    msg['Subject'] = "Emotion Monitoring Alert"
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, ALERT_EMAIL, msg.as_string())
    server.quit()

# Function to analyze emotion from a captured image
def analyze_emotion(frame, patient_id):
    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = analysis[0]['dominant_emotion']
        
        conn = sqlite3.connect("emotion_logs.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO emotions (patient_id, emotion) VALUES (?, ?)", (patient_id, emotion))
        conn.commit()
        conn.close()
        
        # Trigger alert if negative emotion is detected
        if emotion in ['sad', 'angry', 'fear', 'disgust']:
            send_email_alert(patient_id, emotion)
        
        return emotion
    except Exception as e:
        print("Error in emotion detection:", e)
        return None

# Function to capture images from Raspberry Pi Camera
def capture_and_analyze(patient_id):
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        return analyze_emotion(frame, patient_id)
    return None

# Flask API endpoint to trigger emotion analysis
@app.route("/analyze/<patient_id>", methods=["GET"])
def analyze_patient_emotion(patient_id):
    emotion = capture_and_analyze(patient_id)
    if emotion:
        return jsonify({"patient_id": patient_id, "emotion": emotion})
    return jsonify({"error": "Failed to analyze emotion"}), 500

# Flask API to view emotion logs
@app.route("/emotion_logs", methods=["GET"])
def get_logs():
    conn = sqlite3.connect("emotion_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emotions ORDER BY timestamp DESC")
    logs = cursor.fetchall()
    conn.close()
    return jsonify({"logs": logs})

# Real-time Monitoring Dashboard
@app.route("/")
def dashboard():
    conn = sqlite3.connect("emotion_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emotions ORDER BY timestamp DESC LIMIT 10")
    logs = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html", logs=logs)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004, debug=True)
