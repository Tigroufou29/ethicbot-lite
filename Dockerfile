# ---- Base ----
FROM debian:bookworm-slim

# ---- Installer les dépendances ----
RUN apt-get update && apt-get install -y \
    git build-essential python3 python3-pip python3-venv wget curl cmake libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

# ---- Cloner et construire llama.cpp avec correction ----
RUN git clone https://github.com/ggerganov/llama.cpp.git /llama.cpp && \
    cd /llama.cpp && \
    mkdir build && cd build && \
    cmake .. -DLLAMA_CURL=ON -DLLAMA_CUBLAS=OFF -DLLAMA_METAL=OFF && \
    cmake --build . --config Release && \
    # Recherche du binaire principal
    if [ -f bin/main ]; then echo "Binaire trouvé dans bin/main"; \
    elif [ -f main ]; then echo "Binaire trouvé dans build/main"; mv main bin/main; \
    else echo "ERREUR: Binaire non trouvé!"; exit 1; fi

# ---- Copier les fichiers de l'application ----
WORKDIR /
COPY . .

# ---- Vérification et correction des templates ----
RUN echo "=== VÉRIFICATION DES TEMPLATES ===" && \
    echo "1. Contenu du dossier templates avant correction:" && ls -la /templates && \
    echo "2. Création du dossier templates si nécessaire" && mkdir -p /templates && \
    echo "3. Copie manuelle des templates" && cp -r templates/* /templates/ && \
    echo "4. Contenu du dossier templates après correction:" && ls -la /templates && \
    echo "5. Vérification spécifique de chat.html:" && [ -f /templates/chat.html ] && echo "chat.html EXISTE" || echo "chat.html INTROUVABLE" && \
    echo "6. Correction des permissions:" && chmod a+r /templates/chat.html && \
    echo "7. Permissions finales:" && stat -c "%A %n" /templates/chat.html

# ---- Vérifications critiques ----
RUN echo "=== VÉRIFICATION DES FICHIERS ===" && \
    echo "1. Fichiers à la racine:" && ls -la && \
    echo "2. Structure des dossiers:" && tree -L 3 / && \
    echo "3. Contenu du dossier templates:" && ls -la /templates && \
    echo "4. Existence de chat.html:" && [ -f /templates/chat.html ] && echo "PRÉSENT" || echo "ABSENT" && \
    echo "5. Contenu du dossier llama.cpp/build/bin:" && ls -la /llama.cpp/build/bin && \
    echo "6. Existence de l'exécutable:" && [ -f /llama.cpp/build/bin/main ] && echo "main existe!" || echo "main introuvable!" && \
    echo "7. Version de Python:" && python3 --version

# ---- Télécharger le modèle Mistral ----
RUN wget -O /Lite-Mistral-150M-v2-Instruct-FP16.gguf \
"https://huggingface.co/Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16/resolve/main/Lite-Mistral-150M-v2-Instruct-FP16.gguf?download=true"

# ---- Créer un environnement virtuel et installer les dépendances ----
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ---- Rendre le script start.sh exécutable ----
RUN chmod +x start.sh

# ---- Vérification finale ----
RUN echo "=== VÉRIFICATION FINALE ===" && \
    echo "1. Environnement virtuel:" && ls -la /venv/bin && \
    echo "2. Contenu de start.sh:" && cat start.sh && \
    echo "3. Vérification de app.py:" && head -n 20 app.py | grep -A 10 "@app.route"

# ---- Installer tree pour le débogage ----
RUN apt-get update && apt-get install -y tree && rm -rf /var/lib/apt/lists/*

# ---- Exposer le port ----
EXPOSE 8080

# ---- Commande de lancement avec logging ----
CMD ["sh", "-c", "python3 app.py >> /var/log/app.log 2>&1"]
