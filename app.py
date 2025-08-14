import subprocess
import os
import logging
from flask import Flask, request, jsonify, render_template

# Configuration explicite de l'application
app = Flask(
    __name__,
    template_folder='/templates',
    static_folder=None
)
app.logger.setLevel(logging.INFO)

# Chemins des fichiers
MODEL_PATH = "/Lite-Mistral-150M-v2-Instruct-FP16.gguf"
LLAMA_CPP_EXECUTABLE = "/llama.cpp/build/bin/main"
TEMPLATE_PATH = "/templates/chat.html"

# Vérification des chemins au démarrage
def verify_paths():
    paths = {
        "Model": MODEL_PATH,
        "Llama Executable": LLAMA_CPP_EXECUTABLE,
        "Template": TEMPLATE_PATH
    }
    
    for name, path in paths.items():
        if not os.path.exists(path):
            app.logger.error(f"ERREUR: {name} introuvable à {path}")
        else:
            app.logger.info(f"{name} trouvé à {path}")

# Routes
@app.route("/")
def home():
    return "Lite Mistral API OK"

@app.route("/chat", methods=["GET"])
def chat_interface():
    app.logger.info("Accès à l'interface de chat")
    return render_template("chat.html")

@app.route("/api/chat", methods=["POST"])
def chat_api():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Requête JSON invalide"}), 400
    
    prompt = data["prompt"]
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
        return jsonify({"response": output})
    except Exception as e:
        app.logger.error(f"Erreur: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Configuration supplémentaire
    app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    
    # Vérification des chemins
    verify_paths()
    
    # Log des routes
    app.logger.info("Routes enregistrées:")
    for rule in app.url_map.iter_rules():
        app.logger.info(f"{rule.methods}: {rule.rule}")
    
    # Démarrage du serveur
    app.run(
        host="0.0.0.0", 
        port=8080,
        use_reloader=False,
        threaded=True
    )
