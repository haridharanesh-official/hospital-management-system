import smtplib
import ssl
import sqlite3
import json
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client
import requests
from config import (
    EMAIL_HOST, EMAIL_PORT, EMAIL_USER, EMAIL_PASSWORD,
    TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER,
    FCM_SERVER_KEY, DATABASE_PATH
)

class NotificationService:
    def __init__(self):
        self.sms_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    def send_email(self, to_email, subject, body, priority="General", retries=3):
        """ Sends an email with retry logic. """
        for attempt in range(retries):
            try:
                msg = MIMEMultipart()
                msg['From'] = EMAIL_USER
                msg['To'] = to_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'html'))

                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, context=context) as server:
                    server.login(EMAIL_USER, EMAIL_PASSWORD)
                    server.sendmail(EMAIL_USER, to_email, msg.as_string())

                print(f"✅ Email sent to {to_email}")
                self.log_notification("Email", to_email, subject, priority)
                return
            except Exception as e:
                print(f"❌ Email attempt {attempt + 1} failed: {str(e)}")
                time.sleep(2)  # Wait before retrying

    def send_sms(self, to_number, message, priority="General", retries=3):
        """ Sends an SMS with retry logic. """
        for attempt in range(retries):
            try:
                self.sms_client.messages.create(
                    body=message,
                    from_=TWILIO_PHONE_NUMBER,
                    to=to_number
                )
                print(f"✅ SMS sent to {to_number}")
                self.log_notification("SMS", to_number, message, priority)
                return
            except Exception as e:
                print(f"❌ SMS attempt {attempt + 1} failed: {str(e)}")
                time.sleep(2)

    def send_push_notification(self, device_token, title, message, priority="General", retries=3):
        """ Sends a push notification using Firebase with retry logic. """
        url = "https://fcm.googleapis.com/fcm/send"
        headers = {
            "Authorization": f"key={FCM_SERVER_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "to": device_token,
            "notification": {"title": title, "body": message, "priority": priority}
        }
        for attempt in range(retries):
            try:
                response = requests.post(url, headers=headers, data=json.dumps(payload))
                if response.status_code == 200:
                    print(f"✅ Push notification sent to {device_token}")
                    self.log_notification("Push", device_token, title, priority)
                    return
                else:
                    print(f"❌ Push notification attempt {attempt + 1} failed: {response.text}")
            except Exception as e:
                print(f"❌ Push notification attempt {attempt + 1} failed: {str(e)}")
            time.sleep(2)

    def log_notification(self, method, recipient, message, priority):
        """ Logs notifications in the database. """
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notifications (method, recipient, message, priority, timestamp)
                VALUES (?, ?, ?, ?, datetime('now'))
            """, (method, recipient, message, priority))
            conn.commit()
            conn.close()
            print(f"📊 Notification logged: {method} -> {recipient}")
        except Exception as e:
            print(f"❌ Failed to log notification: {str(e)}")

