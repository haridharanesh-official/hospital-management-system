CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    role TEXT CHECK(role IN ('patient', 'staff', 'doctor')) NOT NULL,
    email TEXT UNIQUE NOT NULL,
    contact TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS patient_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    diagnosis TEXT,
    treatment_plan TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS staff_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    staff_id INTEGER,
    shift_date TEXT,
    start_time TEXT,
    end_time TEXT,
    FOREIGN KEY (staff_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    method TEXT,  -- Email, SMS, or Push
    recipient TEXT,  -- Email address, phone number, or device token
    message TEXT,
    priority TEXT CHECK(priority IN ('Emergency', 'Routine', 'General')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS notifications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    method TEXT,  -- Email, SMS, or Push
    recipient TEXT,  -- Email address, phone number, or device token
    message TEXT,
    priority TEXT CHECK(priority IN ('Emergency', 'Routine', 'General')),
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO users (name, role, email, contact) VALUES 
('John Doe', 'patient', 'johndoe@example.com', '123-456-7890'),
('Jane Smith', 'doctor', 'janesmith@example.com', '987-654-3210'),
('Emily Davis', 'staff', 'emilydavis@example.com', '456-789-0123');

INSERT INTO patient_records (user_id, diagnosis, treatment_plan) VALUES 
(1, 'Hypertension', 'Lifestyle modification and medication');

INSERT INTO staff_schedules (staff_id, shift_date, start_time, end_time) VALUES 
(3, '2025-01-15', '08:00', '16:00');
