import cv2
import numpy as np
import mediapipe as mp
import smtplib
from email.mime.text import MIMEText
from flask import Flask, Response
import time
from notification import NotificationService

app = Flask(__name__)

notification = NotificationService()

# Load pre-trained face detection model (Haar cascade or DNN)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Initialize MediaPipe Pose for fall detection
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize webcam
video_capture = cv2.VideoCapture(0)

def send_email_alert():
    sender_email = "haridharanesh.sp@gmail.com"
    receiver_email = "ak6811182@gmail.com"
    password = "hari041007"
    
    msg = MIMEText("Fall detected! Immediate attention required.")
    msg["Subject"] = "Emergency Alert: Fall Detected"
    msg["From"] = sender_email
    msg["To"] = receiver_email
    
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        print("Failed to send email:", e)

def detect_fall(landmarks):
    if landmarks:
        nose_y = landmarks[mp_pose.PoseLandmark.NOSE.value].y
        left_ankle_y = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y
        right_ankle_y = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value].y
        
        # Simple fall detection logic: if nose is close to ankle level
        if nose_y > left_ankle_y and nose_y > right_ankle_y:
            return True
    return False

def generate_frames():
    fall_alert_sent = False
    while True:
        success, frame = video_capture.read()
        if not success:
            break
        
        # Convert frame to grayscale for detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        
        # Convert frame to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)
        
        fall_detected = False
        if results.pose_landmarks:
            fall_detected = detect_fall(results.pose_landmarks.landmark)
        
        # Draw rectangles around detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        if fall_detected:
            cv2.putText(frame, "FALL DETECTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
            if not fall_alert_sent:
                send_email_alert()
                fall_alert_sent = True
        else:
            fall_alert_sent = False
        
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

def check_patient_critical(patient):
    if patient["heart_rate"] > 120:
        subject = "🚨 Urgent: High Heart Rate Detected!"
        body = f"<p>Patient <b>{patient['name']}</b> has a critical heart rate of {patient['heart_rate']} BPM.</p>"
        
        # Send Email & SMS to Doctor
        notification.send_email("doctor@example.com", subject, body, priority="Emergency")
        notification.send_sms("+918508511975", f"🚨 Alert: {patient['name']} has a heart rate of {patient['heart_rate']} BPM.", priority="Emergency")
        
        # Push Notification to Nurse App
        notification.send_push_notification(patient["device_token"], "🚨 High Heart Rate Alert", f"{patient['name']} has a critical heart rate of {patient['heart_rate']} BPM.", priority="Emergency")

@app.route('/monitor')
def monitor():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
