import os
import logging
import requests
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder="templates")
app.logger.setLevel(logging.INFO)

# --- CONFIGURATION ---
HF_MODEL = "Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16"
HF_TOKEN = os.environ.get("HF_TOKEN")  # ton token HuggingFace injecté dans Koyeb

HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}
API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

# --- ROUTES ---

@app.route("/")
def home():
    return "Lite Mistral API OK"

@app.route("/chat")
def chat_interface():
    return render_template("chat.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    prompt = data.get("prompt", "")
    app.logger.info(f"Prompt reçu: {prompt}")

    try:
        response = requests.post(API_URL, headers=HEADERS, json={"inputs": prompt})
        response.raise_for_status()
        output = response.json()

        # HuggingFace retourne parfois un dict ou une liste de dict
        if isinstance(output, list) and "generated_text" in o_
