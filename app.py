import os
import logging
import requests
from flask import Flask, request, jsonify, render_template

# Répertoire de base (là où est app.py)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Flask setup
app = Flask(__name__, template_folder=os.path.join(BASE_DIR, "templates"))
app.logger.setLevel(logging.INFO)

# Modèle Hugging Face (léger)
HF_MODEL = "tiiuae/falcon-rw-1b"   # ⚡ tu peux remplacer par un autre modèle
HF_API_URL = f"https://api-inference.huggingface.co/models/{HF_MODEL}"

# Récupération du token dans Koyeb (Settings > Environment Variables > HF_TOKEN)
HF_TOKEN = os.environ.get("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"} if HF_TOKEN else {}

# Page d’accueil
@app.route("/")
def home():
    return "Lite EthicBot API OK (via Hugging Face)"

# Interface web
@app.route("/chat", methods=["GET"])
def chat_interface():
    return render_template("chat.html")

# Endpoint API
@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    prompt = data.get("prompt", "")
    app.logger.info(f"Prompt reçu: {prompt}")

    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.7}
    }

    try:
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()

        # Hugging Face renvoie une liste ou un dict
        if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
            output = result[0]["generated_text"]
        else:
            output = str(result)

        return jsonify({"response": output})

    except Exception as e:
        app.logger.error(f"Erreur Hugging Face: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
