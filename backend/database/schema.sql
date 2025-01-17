INSERT INTO users (username, password, role) VALUES
('admin', 'admin123', 'admin'),
('doctor1', 'doctorpass', 'doctor'),
('nurse1', 'nursepass', 'nurse');

INSERT INTO staff (name, role, shift, contact) VALUES
('Dr. John Doe', 'Doctor', 'Day', 'john.doe@example.com'),
('Dr. Jane Smith', 'Doctor', 'Night', 'jane.smith@example.com'),
('Nurse Amy White', 'Nurse', 'Day', 'amy.white@example.com'),
('Nurse Bob Brown', 'Nurse', 'Night', 'bob.brown@example.com');

INSERT INTO shifts (staff_id, date, start_time, end_time) VALUES
(1, '2025-01-15', '08:00', '17:00'),
(2, '2025-01-15', '20:00', '06:00'),
(3, '2025-01-15', '08:00', '17:00'),
(4, '2025-01-15', '20:00', '06:00');

INSERT INTO patient_data (patient_id, heart_rate, fall_detected) VALUES
('P001', 75, 0),
('P002', 85, 1),
('P003', 65, 0);

INSERT INTO therapy_schedule (patient_id, therapy, schedule_time, status) VALUES
('P001', 'Physical Therapy', '2025-01-16 10:00', 'Scheduled'),
('P002', 'Speech Therapy', '2025-01-16 14:00', 'Scheduled');
