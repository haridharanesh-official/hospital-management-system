# Hospital Management AI System

This repository contains the code and instructions to set up the **Hospital Management AI System**. This system includes several modules, including AI-driven patient monitoring, digital twin for health monitoring, adaptive therapy scheduling, contextual medical AI assistant, and cybersecurity.

---

## Features

- Patient Health Monitoring via ESP8266 and Raspberry Pi
- AI-powered Contextual Medical Assistant
- Adaptive Therapy Scheduler with Predictive AI
- Cybersecurity & Intrusion Detection
- Digital Twin Integration
- Role-based Access System for doctors, nurses, and admins
- Real-time alerts and notifications (Email/SMS)

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Initial Setup](#initial-setup)
3. [Modules Overview](#modules-overview)
4. [API Integrations](#api-integrations)
5. [How to Run](#how-to-run)
6. [Usage Instructions](#usage-instructions)
7. [Troubleshooting](#troubleshooting)

---

## System Requirements

- Raspberry Pi 5 (8GB variant recommended)
- ESP8266 module for patient monitoring
- Python 3.9 or higher
- Virtual environment setup for Python
- Internet connection

---

## Initial Setup

Follow these steps to set up the project:

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/hospital-management-system.git
cd hospital-management-system
```

### 2. Set Up Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file in the `backend` directory and add the following:

```env
ACCESS_KEY="<Your Picovoice Access Key>"
SMTP_EMAIL="<Your Email Address>"
SMTP_PASSWORD="<Your Email Password>"
API_KEY="<Your SMS/Email Notification API Key>"
```

---

## Modules Overview

### 1. AI Assistant Module

- Runs on Raspberry Pi 5 using the Ollama MedLlama model.
- Wake word: "mahi" (customizable via Porcupine API).
- Provides role-specific responses for doctors, nurses, and admins.

### 2. Digital Twin Module

- Monitors patient data in real-time from ESP8266.
- Sends alerts for abnormal conditions.
- Integrates with Raspberry Pi camera for movement detection.

### 3. Adaptive Therapy Scheduler

- Uses AI for predictive therapy recommendations.
- Provides a dashboard UI for therapy management.
- Sends therapy updates via email/SMS.

---

## API Integrations

### 1. **Picovoice (Porcupine) Wake Word API**

- URL: [Porcupine Developer Console](https://console.picovoice.ai/)
- Steps:
  1. Sign up and create a new project.
  2. Generate your access key.
  3. Replace `<Your Picovoice Access Key>` in the `.env` file.

### 2. **Ollama AI Model (MedLlama)**

- URL: [Ollama AI](https://ollama.ai/)
- Steps:
  1. Download the MedLlama model for Raspberry Pi.
  2. Place the model file in the `models` directory.

### 3. **Email/SMS Alerts**

- Service: Any SMTP email service (e.g., Gmail, SendGrid) or SMS Gateway API (e.g., Twilio).
- Steps:
  1. Configure the SMTP details in the `.env` file.
  2. For Twilio, set the API key and sender number in `.env`.

---

## How to Run

### 1. Start the Backend Server

```bash
cd backend
python3 main.py
```

### 2. Access the Frontend

Navigate to `http://<raspberry-pi-ip>:5000` in your web browser.

---

## Usage Instructions

### 1. Login

- Visit the website.
- Use the following roles for initial login:
  - **Doctor**: `doctor@example.com` / `password123`
  - **Nurse**: `nurse@example.com` / `password123`
  - **Admin**: `admin@example.com` / `adminpass`

### 2. Key Features

#### a. Patient Monitoring

- View patient vitals in real-time.
- Monitor historical trends and generate PDF reports.

#### b. Therapy Scheduler

- View AI-suggested therapy schedules.
- Adjust manually as needed.

#### c. AI Assistant

- Activate using the wake word "mahi."
- Get responses based on role-specific queries.

---

## Troubleshooting

### Common Errors

1. **Error: Missing 'access\_key' in Porcupine setup**

   - Fix: Add your access key in `ai_assistant.py` or `.env`.

2. **ModuleNotFoundError: No module named 'flask\_cors'**

   - Fix: Run `pip install flask-cors` in the virtual environment.

3. **Cannot Connect to ESP8266**

   - Fix: Ensure the ESP8266 module is powered and connected to the network.

---

## Contributing

We welcome contributions! Please create a pull request or open an issue for suggestions.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contact

For support or questions, please contact:

- Email: [support@yourdomain.com](mailto\:support@yourdomain.com)

