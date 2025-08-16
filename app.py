import os
import logging
from flask import Flask, request, jsonify, render_template
from transformers import pipeline
from threading import Lock

# --- Configuration Flask ---
app = Flask(__name__, template_folder="templates")
app.logger.setLevel(logging.INFO)

# --- Modèle public Hugging Face ---
MODEL_ID = "bigscience/bloom-560m"
model_lock = Lock()  # Pour sécuriser l'accès simultané

try:
    text_generator = pipeline("text-generation", model=MODEL_ID)
    app.logger.info(f"Modèle chargé: {MODEL_ID}")
except Exception as e:
    app.logger.error(f"Erreur lors du chargement du modèle: {str(e)}")
    text_generator = None

# --- Page d'accueil ---
@app.route("/")
def home():
    return "Modèle Bloom 560M API OK"

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
    if text_generator is None:
        return jsonify({"error": "Modèle non disponible."}), 500

    prompt = request.json.get("prompt", "")
    app.logger.info(f"Prompt reçu: {prompt}")

    try:
        # Bloque l'accès simultané au modèle pour éviter des crashs
        with model_lock:
            output = text_generator(
                prompt,
                max_new_tokens=200,
                do_sample=True,
                temperature=0.7
            )
        text = output[0]["generated_text"]
        return jsonify({"response": text})
    except Exception as e:
        app.logger.error(f"Erreur génération texte: {str(e)}")
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

    # Démarrage Flask
    app.run(host="0.0.0.0", port=8080)
