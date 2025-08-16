import os
import logging
import requests
from flask import Flask, request, jsonify, render_template

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.logger.setLevel(logging.INFO)

HF_MODEL = "tiiuae/falcon-rw-1b"
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
HF_TOKEN = os.environ.get("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

@app.route("/")
def home():
    return "Lite Mistral API OK (via Hugging Face)"

@app.route("/chat")
def chat_interface():
    return render_template("chat.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    prompt = data.get("prompt", "")
    app.logger.info(f"Prompt reçu: {prompt}")
    payload = {"inputs": prompt, "parameters": {"max_new_tokens":200,"temperature":0.7}}
    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        output = result[0]["generated_text"] if isinstance(result,list) else result.get("generated_text", str(result))
        return jsonify({"response": output})
    except Exception as e:
        app.logger.error(f"Erreur Hugging Face: {str(e)}")
        return jsonify({"error": str(e)}),500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
