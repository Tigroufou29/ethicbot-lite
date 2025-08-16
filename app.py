import os
import logging
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='templates')
app.logger.setLevel(logging.INFO)

# Ton modèle HuggingFace léger
MODEL_REPO = "Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16"
HF_TOKEN = "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"  # Ton token HuggingFace

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

# Page d'accueil
@app.route("/")
def home():
    return "Lite Mistral API OK"

# Interface de chat - GET
@app.route("/chat", methods=["GET"])
def chat_interface():
    app.logger.info("Accès à l'interface de chat")
    try:
        return render_template("chat.html")
    except Exception as e:
        app.logger.error(f"Erreur de rendu du template: {str(e)}")
        return f"Erreur: {str(e)}", 500

# Endpoint API pour le chat - POST
@app.route("/api/chat", methods=["POST"])
def chat_api():
    prompt = request.json.get("prompt", "")
    app.logger.info(f"Prompt reçu: {prompt}")
    
    url = f"https://api-inference.huggingface.co/models/{MODEL_REPO}"
    payload = {"inputs": prompt, "parameters": {"max_new_tokens": 200, "temperature": 0.7}}
    
    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=120)
        response.raise_for_status()
        output = response.json()

        # Récupérer le texte généré
        if isinstance(output, list) and "generated_text" in output[0]:
            text = output[0]["g]()
