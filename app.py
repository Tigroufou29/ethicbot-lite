from flask import Flask, request, jsonify
from huggingface_hub import InferenceClient
import os
import logging

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Récupération du token depuis la variable d'environnement Koyeb
HF_TOKEN = os.environ.get("KOYEB_HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("Le token Hugging Face n'est pas défini dans KOYEB_HF_TOKEN")

# Initialisation du client Hugging Face
client = InferenceClient(token=HF_TOKEN)

# ID du modèle
MODEL_ID = "Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16"

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.json
    prompt = data.get("prompt", "")
    logging.info(f"Prompt reçu: {prompt}")

    try:
        output = client.text_generation(
            model=MODEL_ID,
            prompt=prompt,
            max_new_tokens=150
        )

        # output est une liste de dicts avec la clé "generated_text"
        if isinstance(output, list) and "generated_text" in output[0]:
            text = output[0]["generated_text"]
        else:
            text = "Erreur lors de la génération du texte."

        return jsonify({"response": text})

    except Exception as e:
        logging.error(f"Erreur HuggingFace API: {e}")
        return jsonify({"response": "Erreur lors de la génération du texte."}), 500

@app.route("/chat")
def chat_page():
    # Ici tu peux mettre le HTML de ta page si nécessaire
    return "<h1>Page chat OK</h1>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
