from flask import Blueprint, request, jsonify
import ollama

ai_routes = Blueprint('ai_routes', __name__)

@ai_routes.route("/ask_ai", methods=["POST"])
def ask_ai():
    data = request.json
    user_query = data.get("query")
    
    if not user_query:
        return jsonify({"error": "Query is required"}), 400
    
    try:
        response = ollama.chat(model="medllama", messages=[{"role": "user", "content": user_query}])
        return jsonify({"response": response["message"]["content"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
