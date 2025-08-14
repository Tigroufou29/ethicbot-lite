import subprocess
import os
import logging
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

MODEL_PATH = "/Lite-Mistral-150M-v2-Instruct-FP16.gguf"
LLAMA_CPP_EXECUTABLE = "/llama.cpp/build/bin/main"

# Vérifier que l'exécutable existe
if not os.path.exists(LLAMA_CPP_EXECUTABLE):
    app.logger.error(f"Llama executable not found at {LLAMA_CPP_EXECUTABLE}")

# Endpoint API pour le chat (POST)
@app.route("/api/chat", methods=["POST"])
def chat():
    prompt = request.json.get("prompt", "")
    app.logger.info(f"Received prompt: {prompt}")
    
    cmd = [
        LLAMA_CPP_EXECUTABLE,
        "-m", MODEL_PATH,
        "-p", prompt,
        "-n", "200"
    ]
    
    try:
        app.logger.info(f"Executing command: {' '.join(cmd)}")
        output = subprocess.check_output(cmd, universal_newlines=True)
        return jsonify({"response": output})
    except Exception as e:
        app.logger.error(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Interface de chat (GET) - CORRECTION IMPORTANTE : chemin différent
@app.route("/chat-ui")
def chat_interface():
    app.logger.info("Serving chat interface")
    return render_template("chat.html")

# Page d'accueil
@app.route("/")
def home():
    return "Lite Mistral API OK"

if __name__ == "__main__":
    # Afficher toutes les routes pour le débogage
    print("Registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"{rule.methods}: {rule.rule}")
    
    app.run(host="0.0.0.0", port=8080)
