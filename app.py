import subprocess
import os
import logging
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Configuration des chemins
MODEL_PATH = "/Lite-Mistral-150M-v2-Instruct-FP16.gguf"
LLAMA_CPP_EXECUTABLE = "/llama.cpp/build/bin/main"
TEMPLATE_DIR = "/templates"

# Définir explicitement le dossier des templates
app.template_folder = TEMPLATE_DIR

# Vérification des chemins au démarrage
def log_path_verification():
    paths_to_check = {
        "Template Directory": TEMPLATE_DIR,
        "Template File": os.path.join(TEMPLATE_DIR, "chat.html"),
        "Llama Executable": LLAMA_CPP_EXECUTABLE,
        "Model File": MODEL_PATH
    }
    
    for name, path in paths_to_check.items():
        if os.path.exists(path):
            app.logger.info(f"✅ {name} trouvé: {path}")
        else:
            app.logger.error(f"❌ {name} INTROUVABLE: {path}")

# Route d'accueil
@app.route('/')
def home():
    return "Lite Mistral API OK"

# Route GET pour l'interface de chat
@app.route('/chat', methods=['GET'])
def chat_interface():
    app.logger.info("Accès à l'interface de chat")
    try:
        return render_template('chat.html')
    except Exception as e:
        app.logger.error(f"Erreur de rendu du template: {str(e)}")
        return f"Erreur: {str(e)}", 500

# Route POST pour l'API de chat
@app.route('/api/chat', methods=['POST'])
def chat_api():
    try:
        data = request.get_json()
        prompt = data.get('prompt', '')
        app.logger.info(f"Prompt reçu: {prompt}")
        
        if not prompt:
            return jsonify({"error": "Prompt vide"}), 400
        
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

if __name__ == '__main__':
    # Vérification des chemins
    log_path_verification()
    
    # Journalisation des routes
    app.logger.info("Routes enregistrées:")
    for rule in app.url_map.iter_rules():
        app.logger.info(f"{rule.methods} {rule.rule}")
    
    # Démarrer l'application
    app.run(
        host='0.0.0.0',
        port=8080,
        debug=False,
        use_reloader=False
    )
