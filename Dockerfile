# Configuration de Flask
app = Flask(
    __name__,
    template_folder='templates',  # Chemin relatif au répertoire de travail
    static_folder=None
)

# Définition du chemin du template
TEMPLATE_PATH = "templates/chat.html"  # Chemin relatif

# Dans la fonction chat_interface
@app.route('/chat')
def chat_interface():
    try:
        # Chemin relatif
        template_path = "templates/chat.html"
        
        # Vérification locale
        if not os.path.exists(template_path):
            # Vérifier dans le répertoire parent
            parent_path = "../templates/chat.html"
            if os.path.exists(parent_path):
                return render_template(parent_path)
            
            # Recherche approfondie
            found_paths = []
            for root, dirs, files in os.walk('.'):
                if "chat.html" in files:
                    found_paths.append(os.path.join(root, "chat.html"))
            
            if found_paths:
                return f"Template trouvé à: {', '.join(found_paths)}", 200
            else:
                return "Template introuvable dans le système de fichiers", 500
        
        return render_template('chat.html')
    
    except Exception as e:
        return f"Erreur: {str(e)}", 500
