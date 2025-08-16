import os
import logging
from flask import Flask, request, jsonify, render_template
from huggingface_hub import InferenceClient

# --- CONFIGURATION ---
app = Flask(__name__, template_folder='templates')
app.logger.setLevel(logging.INFO)

HF_TOKEN = "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"  # Ton token HuggingFace
MODEL_NAME = "Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16"

client = InferenceClient(token=HF_TOKEN)

# --- ROUTES ---

# Page d'accueil
@app.route("/")
def home():
    return "Lite Mistral API OK"

# Interface de chat
@app.route("/chat", methods=["GET"])
def chat_interface():
    app.logger.info("Accès à l'interface de chat")
    try:
        return render_template("chat.html")
    except Exception as e:
        app.logger.error(f"Erreur de rendu du template: {str(e)}")
        return f"Erreur: {str(e)}", 500

# Endpoint API pour le chat
@app.route("/api/chat", methods=["POST"])
def chat_api():
    prompt = request.json.get("prompt", "")
    app.logger.info(f"Prompt reçu: {prompt}")

    try:
        output = client.text_generation(
            model=MODEL_NAME,
            inputs=prompt,
            max_new_tokens=200,
            temperature=0.7
        )

        # Récupération du texte généré
        if isinstance(output, list) and "generated_text" in output[0]:
            text = outpu
