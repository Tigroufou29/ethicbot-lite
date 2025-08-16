import os
import logging
from flask import Flask, request, jsonify, render_template
from huggingface_hub import InferenceClient

# --- CONFIGURATION ---
app = Flask(__name__, template_folder='templates')
app.logger.setLevel(logging.INFO)

HF_TOKEN = os.getenv("HF_TOKEN")
MODEL_NAME = "Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16"

if not HF_TOKEN:
    raise ValueError("⚠️ La variable d'environnement HF_TOKEN n'est pas définie sur Koyeb")

client = InferenceClient(token=HF_TOKEN)

# --- ROUTES ---
@app.route("/")
def home():
    return "✅ Lite Mistral API déployée sur Koyeb"

@app.route("/chat", methods=["GET"])
def chat_interface():
    try:
        return render_template("chat.html")
    except Exception as e:
        app.logger.error(f"Erreur template: {str(e)}")
        return f"Erreur: {str(e)}", 500

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

        if isinstance(output, list) and "generated_text" in output[0]:
            text = output[0]["generated_text"]
        elif isinstance(output, dict) and "generated_text" in output:
            text = output["generated_text"]
        elif isinstance(output, dict) and "error" in output:
            text = f"Erreur HuggingFace: {output['error']}"
        else:
            text = str(output)

        return jsonify({"response":
