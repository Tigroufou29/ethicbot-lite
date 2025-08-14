import subprocess
import os
import logging
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Configuration des chemins
MODEL_PATH = "/Lite-Mistral-150M-v2-Instruct-FP16.gguf"
LLAMA_CPP_EXECUTABLE = "/llama.cpp/build/bin/main"

# Route d'accueil
@app.route('/')
def home():
    return "Lite Mistral API OK"

# Route GET pour l'interface de chat - Chemin primaire
@app.route('/chat', methods=['GET'])
def chat_interface():
    app.logger.info("Accès à l'interface de chat via /chat")
    return render_template('chat.html')

# Route alternative pour l'interface
@app.route('/chat-ui', methods=['GET'])
def chat_interface_alt():
    app.logger.info("Accès à l'interface de chat via /chat-ui")
    return render_template('chat.html')

# Route API pour le chat
@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        app.logger.info(f"Prompt reçu: {prompt}")
        
        cmd = [
            LLAMA_CPP_EXECUTABLE,
            "-m", MODEL_PATH,
            "-p", prompt,
            "-n", "200",
            "--temp", "0.7"
        ]
        
        app.logger.info(f"Exécution de la commande: {' '.join(cmd)}")
        output = subprocess.check_output(
            cmd, 
            universal_newlines=True,
            timeout=120
        )
        return jsonify({"response": output})
    except Exception as e:
        app.logger.error(f"Erreur API: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Route de santé pour vérification
@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "routes": {
            "/chat": "GET",
            "/chat-ui": "GET",
            "/api/chat": "POST"
        }
    })

if __name__ == '__main__':
    # Log des routes
    app.logger.info("Routes enregistrées:")
    for rule in app.url_map.iter_rules():
        app.logger.info(f"{rule.methods} -> {rule.rule}")
    
    # Démarrer l'application
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False,
        use_reloader=False
    )
