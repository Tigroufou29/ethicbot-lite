import subprocess
import os
import logging
from flask import Flask, request, jsonify, render_template

# Répertoire de base = emplacement du fichier app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Créer l'application Flask avec le bon chemin des templates
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=None
)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chemins critiques
MODEL_PATH = os.path.join(BASE_DIR, "Lite-Mistral-150M-v2-Instruct-FP16.gguf")
LLAMA_CPP_EXECUTABLE = "/llama.cpp/build/bin/main"
TEMPLATE_PATH = os.path.join(BASE_DIR, "templates", "chat.html")

# Route racine
@app.route('/')
def home():
    logger.info("Accès à la route racine")
    return "Lite Mistral API OK"

# Route GET pour l'interface de chat
@app.route('/chat')
def chat_interface():
    logger.info("Accès à la route /chat")
    try:
        return render_template("chat.html")
    except Exception as e:
        logger.error(f"Erreur de rendu du template: {str(e)}")
        return f"Erreur: {str(e)}", 500

# Route API de chat
@app.route('/api/chat', methods=['POST'])
def chat_api():
    logger.info("Accès à l'API /api/chat")
    try:
        data = request.get_json()
        if not data or 'prompt' not in data:
            return jsonify({"error": "Requête JSON invalide"}), 400

        prompt = data['prompt']
        logger.info(f"Prompt reçu: {prompt}")

        cmd = [
            LLAMA_CPP_EXECUTABLE,
            "-m", MODEL_PATH,
            "-p", prompt,
            "-n", "200",
            "--temp", "0.7"
        ]

        logger.info(f"Exécution de la commande: {' '.join(cmd)}")
        output = subprocess.check_output(
            cmd,
            universal_newlines=True,
            timeout=120
        )

        # Nettoyer la sortie
        cleaned_output = output.split("assistant:")[-1].strip()

        return jsonify({
            "status": "success",
            "response": cleaned_output
        })
    except Exception as e:
        logger.error(f"Erreur API: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Route de diagnostic
@app.route('/debug')
def debug():
    logger.info("Accès à la page de debug")

    # Vérification des chemins
    paths = {
        "app.py": os.path.exists(os.path.join(BASE_DIR, "app.py")),
        "templates/chat.html": os.path.exists(TEMPLATE_PATH),
        "llama.cpp": os.path.exists(LLAMA_CPP_EXECUTABLE),
        "model": os.path.exists(MODEL_PATH)
    }

    # Liste des routes
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            "endpoint": rule.endpoint,
            "methods": sorted(rule.methods),
            "path": str(rule)
        })

    # Vérification des permissions du template
    template_info = {}
    if os.path.exists(TEMPLATE_PATH):
        stat_info = os.stat(TEMPLATE_PATH)
        template_info = {
            "exists": True,
            "size": stat_info.st_size,
            "permissions": oct(stat_info.st_mode),
            "readable": os.access(TEMPLATE_PATH, os.R_OK)
        }
    else:
        template_info = {"exists": False}

    return jsonify({
        "status": "debug",
        "paths": paths,
        "routes": routes,
        "template_info": template_info,
        "environment": dict(os.environ)
    })

if __name__ == '__main__':
    # Journalisation des routes au démarrage
    logger.info("Application démarrée. Routes disponibles:")
    for rule in app.url_map.iter_rules():
        logger.info(f"Route: {rule} | Méthodes: {sorted(rule.methods)}")

    # Démarrer le serveur
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False,
        use_reloader=False
    )
