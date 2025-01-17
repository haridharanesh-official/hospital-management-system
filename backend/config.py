import os

# Database Configuration
DB_NAME = "hospital.db"

# Email Configuration
EMAIL_SENDER = "yourhospital@gmail.com"
EMAIL_PASSWORD = "yourpassword"
STAFF_EMAILS = [
    "staff1@example.com",
    "staff2@example.com",
    "staff3@example.com",
    "staff4@example.com",
    "staff5@example.com"
]

# AI Assistant Configuration
OLLAMA_MODEL = "medllama"
WAKE_WORD = "mahi"

# Cybersecurity Configuration
WHITELISTED_IPS = ["192.168.1.1", "192.168.1.2"]

# Disaster Response API
WEATHER_API_KEY = "your_weather_api_key"
CROWD_PREDICTION_MODEL = "crowd_model.h5"

# IoT Sensor Configuration
ESP8266_IP = "192.168.1.100"
MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883

# Flask Server Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
DEBUG_MODE = True

# Email Configuration
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 465
EMAIL_USER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-app-password"  # Use App Password for security

# Twilio SMS Configuration
TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"  # Twilio phone number

# Firebase Push Notifications
FCM_SERVER_KEY = "your-firebase-server-key"

# Database Path
DATABASE_PATH = "database/hospital.db"
