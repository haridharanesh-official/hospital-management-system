from flask import Blueprint, request, jsonify
import sqlite3

patient_routes = Blueprint('patient_routes', __name__)

def get_db_connection():
    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row
    return conn

@patient_routes.route("/patients", methods=["GET"])
def get_patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_data")
    patients = cursor.fetchall()
    conn.close()
    return jsonify([dict(patient) for patient in patients])

@patient_routes.route("/patients/<patient_id>", methods=["GET"])
def get_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patient_data WHERE patient_id = ?", (patient_id,))
    patient = cursor.fetchone()
    conn.close()
    if patient:
        return jsonify(dict(patient))
    return jsonify({"error": "Patient not found"}), 404

@patient_routes.route("/patients", methods=["POST"])
def add_patient():
    data = request.json
    patient_id = data.get("patient_id")
    heart_rate = data.get("heart_rate")
    fall_detected = data.get("fall_detected", 0)
    
    if not all([patient_id, heart_rate]):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patient_data (patient_id, heart_rate, fall_detected) VALUES (?, ?, ?)",
                   (patient_id, heart_rate, fall_detected))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Patient data added successfully"}), 201
