import subprocess
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

MODEL_PATH = "/Lite-Mistral-150M-v2-Instruct-FP16.gguf"
LLAMA_CPP_EXECUTABLE = "/llama.cpp/build/bin/main"

# Endpoint API pour le chat (POST)
@app.route("/api/chat", methods=["POST"])
def chat():
    prompt = request.json.get("prompt", "")
    cmd = [
        LLAMA_CPP_EXECUTABLE,
        "-m", MODEL_PATH,
        "-p", prompt,
        "-n", "200"
    ]
    try:
        output = subprocess.check_output(cmd, universal_newlines=True)
        return jsonify({"response": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Interface de chat (GET)
@app.route("/chat")
def chat_interface():
    return render_template("chat.html")

# Page d'accueil
@app.route("/")
def home():
    return "Lite Mistral API OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
