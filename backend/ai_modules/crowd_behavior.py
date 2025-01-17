import cv2
import numpy as np
from flask import Flask, request, jsonify, render_template
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)

# Email settings
EMAIL_SENDER = "haridharanesh.sp@gmail.com"
EMAIL_PASSWORD = "hari041007"
ALERT_EMAIL = "ak6811182@gmail.com"

# Function to send email alerts
def send_email_alert(alert_message):
    msg = MIMEText(alert_message)
    msg['From'] = EMAIL_SENDER
    msg['To'] = ALERT_EMAIL
    msg['Subject'] = "Crowd Behavior Alert"
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(EMAIL_SENDER, EMAIL_PASSWORD)
    server.sendmail(EMAIL_SENDER, ALERT_EMAIL, msg.as_string())
    server.quit()

# Crowd behavior detection using OpenCV
def analyze_crowd_behavior(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = cv2.createBackgroundSubtractorMOG2().apply(gray)
    contours, _ = cv2.findContours(fgmask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    crowd_density = sum(cv2.contourArea(cnt) for cnt in contours)
    if crowd_density > 50000:
        send_email_alert("High crowd density detected in hospital premises.")
    
    return crowd_density

# Flask route for video processing
@app.route("/process_video", methods=["POST"])
def process_video():
    file = request.files['video']
    cap = cv2.VideoCapture(file.stream)
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        crowd_density = analyze_crowd_behavior(frame)
        
    cap.release()
    return jsonify({"message": "Video processed", "crowd_density": crowd_density})

# Web dashboard for real-time monitoring
@app.route("/")
def dashboard():
    return render_template("crowd_dashboard.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
