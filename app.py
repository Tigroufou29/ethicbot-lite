import subprocess
import os
import logging
from flask import Flask, request, jsonify, render_template

# Créer l'application Flask avec configuration explicite
app = Flask(
    __name__,
    template_folder='/templates',
    static_folder=None
)

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chemins critiques
MODEL_PATH = "/Lite-Mistral-150M-v2-Instruct-FP16.gguf"
LLAMA_CPP_EXECUTABLE = "/llama.cpp/build/bin/main"

# Route racine
@app.route('/')
def home():
    logger.info("Accès à la route racine")
    return "Lite Mistral API OK"

# Route GET pour l'interface de chat - Version simplifiée
@app.route('/chat')
def chat_interface():
    logger.info("Accès à la route /chat")
    try:
        # Rendu direct sans vérification supplémentaire
        return """
        <!DOCTYPE html>
        <html>
        <body>
            <h1>Interface de chat fonctionnelle!</h1>
            <p>Si vous voyez ce message, le routage Flask fonctionne correctement.</p>
            <p>Prochaine étape: Réactiver chat.html</p>
        </body>
        </html>
        """
    except Exception as e:
        logger.error(f"Erreur de rendu: {str(e)}")
        return f"Erreur: {str(e)}", 500

# Route API de chat
@app.route('/api/chat', methods=['POST'])
def chat_api():
    logger.info("Accès à l'API /api/chat")
    return jsonify({
        "status": "success",
        "message": "L'API fonctionne",
        "response": "Ceci est une réponse de test"
    })

# Route de diagnostic
@app.route('/debug')
def debug():
    logger.info("Accès à la page de debug")
    
    # Vérification des chemins
    paths = {
        "app.py": os.path.exists("/app.py"),
        "templates/chat.html": os.path.exists("/templates/chat.html"),
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
    
    return jsonify({
        "status": "debug",
        "paths": paths,
        "routes": routes,
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
