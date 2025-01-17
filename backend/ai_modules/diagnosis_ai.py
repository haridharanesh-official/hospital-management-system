from flask import Flask, request, jsonify
from ollama import ChatBot  # Example, replace with actual Ollama MedLlama integration
import sqlite3

app = Flask(__name__)

# Initialize AI Model (Replace with actual Ollama MedLlama setup)
ai_bot = ChatBot("ollama run medllama2")

# Database connection setup
def init_db():
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS patients (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        age INTEGER,
                        symptoms TEXT,
                        diagnosis TEXT,
                        treatment TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route("/diagnose", methods=["POST"])
def diagnose():
    data = request.json
    name = data.get("name")
    age = data.get("age")
    symptoms = data.get("symptoms")
    
    if not symptoms:
        return jsonify({"error": "Symptoms required"}), 400
    
    # AI-based diagnosis
    prompt = f"Patient: {name}, Age: {age}, Symptoms: {symptoms}. Provide diagnosis and treatment."
    response = ai_bot.chat(prompt)
    
    # Parse AI response (Assuming structured response)
    diagnosis, treatment = response.split("Treatment:")
    
    # Save to database
    conn = sqlite3.connect("patients.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO patients (name, age, symptoms, diagnosis, treatment) VALUES (?, ?, ?, ?, ?)",
                   (name, age, symptoms, diagnosis.strip(), treatment.strip()))
    conn.commit()
    conn.close()
    
    return jsonify({"diagnosis": diagnosis.strip(), "treatment": treatment.strip()})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
