import os
import subprocess
import pvporcupine
import pyaudio
import struct
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import ollama
import whisper
import pyttsx3
import sqlite3

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Initialize wake word detection
porcupine = pvporcupine.create(keywords=["mahi"])
pa = pyaudio.PyAudio()
stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=porcupine.frame_length)

# Initialize Whisper for Speech-to-Text
whisper_model = whisper.load_model("base")

# Initialize Piper for Text-to-Speech
engine = pyttsx3.init()

# Database setup
def init_db():
    conn = sqlite3.connect("hospital_users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT CHECK(role IN ('doctor', 'nurse', 'admin')) NOT NULL)''')
    conn.commit()
    conn.close()

init_db()

# Role-based query restrictions
role_restrictions = {
    "doctor": ["diagnosis", "treatment", "patient medical history"],
    "nurse": ["patient care", "medication schedule"],
    "admin": ["staff scheduling", "resource allocation"]
}

@app.route("/")
def index():
    if "user" in session:
        return redirect(url_for("dashboard"))
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    conn = sqlite3.connect("hospital_users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
    user = cursor.fetchone()
    conn.close()
    
    if user:
        session["user"] = username
        session["role"] = user[3]
        return jsonify({"message": "Login successful", "role": user[3]})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    role = data.get("role")
    
    if role not in ["doctor", "nurse", "admin"]:
        return jsonify({"error": "Invalid role specified"}), 400
    
    conn = sqlite3.connect("hospital_users.db")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        conn.commit()
        return jsonify({"message": "User registered successfully"})
    except sqlite3.IntegrityError:
        return jsonify({"error": "Username already exists"}), 400
    finally:
        conn.close()

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("index"))
    return render_template("dashboard.html", username=session["user"], role=session["role"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    session.pop("role", None)
    return redirect(url_for("index"))

@app.route("/query", methods=["POST"])
def query():
    if "user" not in session:
        return jsonify({"error": "Unauthorized access"}), 403
    
    data = request.json
    user_input = data.get("text", "")
    role = session["role"]
    
    if not user_input:
        return jsonify({"error": "No input received"}), 400
    
    if not any(keyword in user_input.lower() for keyword in role_restrictions.get(role, [])):
        return jsonify({"error": "Access denied for this query"}), 403
    
    role_based_prompt = {
        "doctor": "Provide a detailed diagnosis and treatment recommendation for: ",
        "nurse": "Give patient care instructions for: ",
        "admin": "Provide hospital resource and staff coordination insights for: "
    }
    
    ai_query = role_based_prompt.get(role, "") + user_input
    response = ollama.chat(model="medllama", message=ai_query)
    
    if role == "doctor":
        priority_notification("Urgent medical query processed.")
    elif role == "nurse":
        priority_notification("Routine patient care guidance updated.")
    
    engine.say(response)
    engine.runAndWait()
    
    return jsonify({"response": response})

def priority_notification(message):
    print(f"[PRIORITY NOTIFICATION]: {message}")

# Function to continuously listen for wake word
def listen_for_wake_word():
    print("Listening for wake word 'mahi'...")
    while True:
        pcm = stream.read(porcupine.frame_length)
        pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
        keyword_index = porcupine.process(pcm)
        if keyword_index >= 0:
            print("Wake word detected! Activating AI Assistant...")
            os.system("mpg123 wake_sound.mp3")  # Optional: play wake sound
            process_voice_command()

# Function to process voice input
def process_voice_command():
    print("Listening for user query...")
    subprocess.run(["arecord", "-d", "5", "-f", "cd", "query.wav"])  # Record audio
    result = whisper_model.transcribe("query.wav")
    user_query = result["text"]
    print(f"User said: {user_query}")
    
    # Process query through Medllama
    response = ollama.chat(model="medllama", message=user_query)
    print(f"AI Response: {response}")
    
    # Convert AI response to speech
    engine.say(response)
    engine.runAndWait()

if __name__ == "__main__":
    subprocess.Popen(listen_for_wake_word)
    app.run(host="0.0.0.0", port=5004, debug=True)
