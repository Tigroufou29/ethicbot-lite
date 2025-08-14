import subprocess
import os
import logging
from flask import Flask, request, jsonify, render_template

app = Flask(__name__, template_folder='/templates')
app.logger.setLevel(logging.INFO)

MODEL_PATH = "/Lite-Mistral-150M-v2-Instruct-FP16.gguf"
LLAMA_CPP_EXECUTABLE = "/llama.cpp/build/bin/main"

# Vérification du chemin de l'exécutable
if not os.path.exists(LLAMA_CPP_EXECUTABLE):
    app.logger.error(f"ERREUR: Exécutable Llama introuvable à {LLAMA_CPP_EXECUTABLE}")
else:
    app.logger.info(f"Exécutable Llama trouvé à {LLAMA_CPP_EXECUTABLE}")

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
    
    cmd = [
        LLAMA_CPP_EXECUTABLE,
        "-m", MODEL_PATH,
        "-p", prompt,
        "-n", "200",
        "--temp", "0.7"
    ]
    
    try:
        app.logger.info(f"Exécution de la commande: {' '.join(cmd)}")
        output = subprocess.check_output(
            cmd, 
            universal_newlines=True,
            timeout=120
        )
        # Nettoyer la sortie
        cleaned_output = output.split("assistant:")[-1].strip()
        return jsonify({"response": cleaned_output})
    except Exception as e:
        app.logger.error(f"Erreur: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Log des routes disponibles
    app.logger.info("Routes enregistrées:")
    for rule in app.url_map.iter_rules():
        app.logger.info(f"{rule.methods}: {rule.rule}")
    
    # Vérification du fichier template
    template_path = "/templates/chat.html"
    if os.path.exists(template_path):
        app.logger.info(f"Template trouvé à {template_path}")
    else:
        app.logger.error(f"ERREUR: Template introuvable à {template_path}")
    
    app.run(host="0.0.0.0", port=8080)
