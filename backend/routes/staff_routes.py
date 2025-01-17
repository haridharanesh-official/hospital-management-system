from flask import Blueprint, request, jsonify
import sqlite3

staff_routes = Blueprint('staff_routes', __name__)

def get_db_connection():
    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row
    return conn

@staff_routes.route("/staff", methods=["GET"])
def get_staff():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM staff")
    staff = cursor.fetchall()
    conn.close()
    return jsonify([dict(member) for member in staff])

@staff_routes.route("/staff/<int:staff_id>", methods=["GET"])
def get_staff_member(staff_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM staff WHERE id = ?", (staff_id,))
    member = cursor.fetchone()
    conn.close()
    if member:
        return jsonify(dict(member))
    return jsonify({"error": "Staff member not found"}), 404

@staff_routes.route("/staff", methods=["POST"])
def add_staff_member():
    data = request.json
    name = data.get("name")
    role = data.get("role")
    shift = data.get("shift")
    contact = data.get("contact")
    
    if not all([name, role, shift, contact]):
        return jsonify({"error": "Missing required fields"}), 400
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO staff (name, role, shift, contact) VALUES (?, ?, ?, ?)",
                   (name, role, shift, contact))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Staff member added successfully"}), 201
