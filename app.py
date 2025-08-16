import os
import logging
from flask import Flask, request, jsonify, render_template
from huggingface_hub import InferenceClient

# --- Configuration Flask ---
app = Flask(__name__, template_folder="templates")
app.logger.setLevel(logging.INFO)

# --- Token Hugging Face Koyeb ---
koyeb_token = os.environ.get("KOYEB_HF_TOKEN", "")
if not koyeb_token:
    app.logger.error("Le token Hugging Face n'est pas défini dans KOYEB_HF_TOKEN.")

# --- Client Hugging Face ---
client = InferenceClient(token=koyeb_token)
# Nouveau modèle public performant
model_id = "tiiuae/falcon-7b-instruct"

# --- Page d'accueil ---
@app.route("/")
def home():
    return "Falcon-7B Instruct API OK"

# --- Interface de chat ---
@app.route("/chat", methods=["GET"])
def chat_interface():
    try:
        return render_template("chat.html")
    except Exception as e:
        app.logger.error(f"Erreur de rendu du template: {str(e)}")
        return f"Erreur: {str(e)}", 500

# --- Endpoint API chat ---
@app.route("/api/chat", methods=["POST"])
def chat_api():
    prompt = request.json.get("prompt", "")
    app.logger.info(f"Prompt reçu: {prompt}")

    try:
        output = client.text_generation(
            model=model_id,
            prompt=prompt,
            max_new_tokens=200,
            temperature=0.7
        )
        text = output[0]["generated_text"]
        return jsonify({"response": text})
    except Exception as e:
        app.logger.error(f"Erreur HuggingFace API: {str(e)}")
        return jsonify({"error": "Erreur lors de la génération du texte."}), 500

# --- Lancement de l'application ---
if __name__ == "__main__":
    template_path = "templates/chat.html"
    if os.path.exists(template_path):
        app.logger.info(f"Template trouvé à {template_path}")
    else:
        app.logger.error(f"ERREUR: Template introuvable à {template_path}")

    app.logger.info("Routes enregistrées:")
    for rule in app.url_map.iter_rules():
        app.logger.info(f"{rule.methods}: {rule.rule}")

    app.run(host="0.0.0.0", port=8080)
