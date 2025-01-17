Step 2: Install Required Dependencies
🏗️ 1. Install Python & Required Libraries
bash
Copy
Edit
sudo apt install python3 python3-pip sqlite3 -y
pip3 install flask flask-cors requests
🛠️ 2. Install Git & Clone the Project
bash
Copy
Edit
sudo apt install git -y
git clone https://github.com/your-repo/hospital-management-system.git
cd hospital-management-system
📌 Step 3: Setup Backend (Flask Server)
Go to the backend folder:

bash
Copy
Edit
cd backend
Install Python dependencies:

bash
Copy
Edit
pip3 install -r requirements.txt
Set up SQLite Database:

bash
Copy
Edit
sqlite3 database/hospital.db < database/schema.sql
Run the Flask Backend:

bash
Copy
Edit
python3 main.py
You should see:
✅ Running on http://0.0.0.0:5000
📌 Step 4: Setup Frontend (Web Dashboard)
Go to the frontend folder:
bash
Copy
Edit
cd ../frontend
Install Dependencies:
bash
Copy
Edit
sudo apt install nginx -y
Start the Web Dashboard:
bash
Copy
Edit
python3 -m http.server 8000
Now visit: http://RaspberryPi_IP:8000/dashboard.html
📌 Step 5: Setup ESP8266 IoT Module
Upload esp8266_code.ino to ESP8266 via Arduino IDE.
Make sure ESP8266 connects to Wi-Fi and sends data to http://RaspberryPi_IP:5000/sensor-data.
Check logs in Flask Backend for ESP8266 data reception.
📌 Step 6: Auto-Start Backend & Frontend on Boot
✅ Make Flask Server Run on Boot
Edit crontab:
bash
Copy
Edit
crontab -e
Add this at the end:
bash
Copy
Edit
@reboot cd /home/pi/hospital-management-system/backend && python3 main.py &
✅ Make Frontend Auto-Start
Edit crontab again:
bash
Copy
Edit
@reboot cd /home/pi/hospital-management-system/frontend && python3 -m http.server 8000 &
📌 Step 7: Access the System
📟 Backend API: http://RaspberryPi_IP:5000
🌐 Dashboard: http://RaspberryPi_IP:8000/dashboard.html
📡 ESP8266 Data Stream: Sent to Raspberry Pi
🎯 Next Steps
✅ Add SSL for Secure Connection
✅ Setup a Public URL for Remote Access
✅ Enable MQTT for IoT Communication
