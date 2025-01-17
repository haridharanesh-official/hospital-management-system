from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
from flask_sqlalchemy import SQLAlchemy
import datetime

# Import AI modules
from ai_modules.ai_assistant import AI_Assistant
from ai_modules.crowd_behavior import CrowdBehaviorAI
from ai_modules.diagnosis_ai import DiagnosisAI
from ai_modules.disaster_response import DisasterResponseAI
from ai_modules.emotion_based_monitoring import EmotionMonitorAI
from ai_modules.health_monitor import HealthMonitorAI
from ai_modules.personalized_medication import MedicationAI
from ai_modules.smart_waste_management import WasteManagementAI
from ai_modules.staff_management import StaffManagementAI
from ai_modules.therapy_scheduler import TherapySchedulerAI

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hospital.db'  # Change to MySQL if needed
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Initialize AI Modules
ai_assistant = AI_Assistant()
crowd_behavior_ai = CrowdBehaviorAI()
diagnosis_ai = DiagnosisAI()
disaster_response_ai = DisasterResponseAI()
emotion_monitor_ai = EmotionMonitorAI()
health_monitor_ai = HealthMonitorAI()
medication_ai = MedicationAI()
waste_management_ai = WasteManagementAI()
staff_management_ai = StaffManagementAI()
therapy_scheduler_ai = TherapySchedulerAI()

class SensorData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)
    heart_rate = db.Column(db.Float, nullable=False)
    spo2 = db.Column(db.Float, nullable=False)
    device_ip = db.Column(db.String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": self.temperature,
            "humidity": self.humidity,
            "heart_rate": self.heart_rate,
            "spo2": self.spo2,
            "device_ip": self.device_ip
        }


# Database connection
def get_db_connection():
    conn = sqlite3.connect('database/hospital.db')
    conn.row_factory = sqlite3.Row
    return conn

# --- AI Assistant Route ---
@app.route("/ai/assistant", methods=["POST"])
def ai_assistant_response():
    data = request.json
    user_query = data.get("query", "")
    response = ai_assistant.process_request(user_query)
    return jsonify({"response": response})

# --- Health Monitoring Route ---
@app.route("/ai/health-monitor", methods=["GET"])
def health_monitor():
    data = health_monitor_ai.get_patient_health()
    return jsonify(data)

# --- Emotion-Based Monitoring Route ---
@app.route("/ai/emotion-monitor", methods=["GET"])
def emotion_monitor():
    data = emotion_monitor_ai.analyze_patient_emotions()
    return jsonify(data)

# --- Personalized Medication Route ---
@app.route("/ai/medication", methods=["POST"])
def medication_recommendation():
    data = request.json
    patient_id = data.get("patient_id")
    if not patient_id:
        return jsonify({"error": "Patient ID required"}), 400
    recommendation = medication_ai.get_medication_plan(patient_id)
    return jsonify(recommendation)

# --- Staff Management Route ---
@app.route("/staff/schedule", methods=["POST"])
def staff_schedule():
    data = request.json
    staff_id = data.get("staff_id")
    shift_time = data.get("shift_time")

    if not staff_id or not shift_time:
        return jsonify({"error": "Staff ID and Shift Time required"}), 400

    result = staff_management_ai.schedule_shift(staff_id, shift_time)
    return jsonify({"message": result})

# --- Crowd Behavior Prediction Route ---
@app.route("/ai/crowd-behavior", methods=["GET"])
def crowd_behavior():
    data = crowd_behavior_ai.analyze_behavior()
    return jsonify(data)

# --- Smart Waste Management Route ---
@app.route("/ai/waste-management", methods=["GET"])
def waste_management():
    data = waste_management_ai.manage_waste()
    return jsonify(data)

# --- Disaster Response Route ---
@app.route("/ai/disaster-response", methods=["GET"])
def disaster_response():
    data = disaster_response_ai.analyze_emergency()
    return jsonify(data)

# --- Therapy Scheduler Route ---
@app.route("/ai/therapy-scheduler", methods=["POST"])
def therapy_schedule():
    data = request.json
    patient_id = data.get("patient_id")
    if not patient_id:
        return jsonify({"error": "Patient ID required"}), 400
    schedule = therapy_scheduler_ai.create_schedule(patient_id)
    return jsonify(schedule)

# --- Hospital Database Route ---
@app.route("/patients", methods=["GET"])
def get_patients():
    conn = get_db_connection()
    patients = conn.execute('SELECT * FROM patients').fetchall()
    conn.close()

    patients_list = [dict(row) for row in patients]
    return jsonify(patients_list)

@app.route("/staff", methods=["GET"])
def get_staff():
    conn = get_db_connection()
    staff = conn.execute('SELECT * FROM staff').fetchall()
    conn.close()

    staff_list = [dict(row) for row in staff]
    return jsonify(staff_list)

@app.route('/api/sensor-data', methods=['POST'])
def receive_sensor_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid data"}), 400

    try:
        new_entry = SensorData(
            temperature=data['temperature'],
            humidity=data['humidity'],
            heart_rate=data['heart_rate'],
            spo2=data['spo2'],
            device_ip=request.remote_addr
        )
        db.session.add(new_entry)
        db.session.commit()

        # Check for abnormal health conditions
        alerts = check_health_alerts(data)

        return jsonify({"message": "Data received successfully", "alerts": alerts}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Route to fetch latest sensor data for dashboard
@app.route('/api/latest-sensor-data', methods=['GET'])
def get_latest_sensor_data():
    latest_data = SensorData.query.order_by(SensorData.timestamp.desc()).first()
    if latest_data:
        return jsonify(latest_data.to_dict())
    return jsonify({"message": "No data available"}), 404

# Function to check abnormal health conditions
def check_health_alerts(data):
    alerts = []
    if data['spo2'] < 90:
        alerts.append("⚠️ Low SpO2 detected! Possible oxygen deficiency.")
    if data['heart_rate'] > 120:
        alerts.append("⚠️ High Heart Rate detected! Possible stress or cardiac issue.")
    if data['temperature'] > 38:
        alerts.append("⚠️ High body temperature detected! Possible fever.")
    return alerts

@app.route("/notifications/<int:notification_id>/mark-read", methods=["POST"])
def mark_notification_as_read(notification_id):
    """ Marks a notification as read. """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE notifications SET is_read = 1 WHERE id = ?", (notification_id,))
    conn.commit()
    conn.close()
    return jsonify({"message": "Notification marked as read"}), 200

# Run Flask server
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)
