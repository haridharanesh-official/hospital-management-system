import sqlite3

def get_db_connection():
    conn = sqlite3.connect("hospital.db")
    conn.row_factory = sqlite3.Row
    return conn

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT)''')
    
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
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS patient_data (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id TEXT,
                        heart_rate INTEGER,
                        fall_detected BOOLEAN,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS therapy_schedule (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        patient_id TEXT,
                        therapy TEXT,
                        schedule_time TEXT,
                        status TEXT)''')
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS intrusion_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        event TEXT,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    conn.commit()
    conn.close()

create_tables()
