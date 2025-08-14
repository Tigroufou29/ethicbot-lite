# ---- Base ----
FROM debian:bookworm-slim

# ---- Installer les dépendances ----
RUN apt-get update && apt-get install -y \
    git build-essential python3 python3-pip python3-venv wget curl cmake libcurl4-openssl-dev \
    && rm -rf /var/lib/apt/lists/*

# ---- Cloner llama.cpp ----
RUN git clone https://github.com/ggerganov/llama.cpp.git /llama.cpp

# ---- Construire llama.cpp avec CMake ----
WORKDIR /llama.cpp
RUN mkdir build && cd build && \
    cmake .. -DLLAMA_CURL=ON -DLLAMA_CUBLAS=OFF -DLLAMA_METAL=OFF && \
    cmake --build . --config Release

# ---- Copier les fichiers de l'application ----
WORKDIR /
COPY app.py .
COPY requirements.txt .
COPY start.sh .
# Ajout du dossier templates pour l'interface de chat
COPY templates /templates

# ---- Vérifications critiques ----
RUN echo "=== VÉRIFICATION DES FICHIERS ===" && \
    echo "1. Fichiers à la racine:" && ls -la && \
    echo "2. Contenu du dossier templates:" && ls -la /templates && \
    echo "3. Aperçu du fichier chat.html:" && head -n 5 /templates/chat.html && \
    echo "4. Exécutable llama.cpp:" && ls -la /llama.cpp/build/bin/main && \
    echo "5. Modèle Mistral (doit être absent à ce stade):" && \
    (ls -la /Lite-Mistral-150M-v2-Instruct-FP16.gguf || echo "Le modèle n'est pas encore téléchargé - c'est normal") && \
    echo "6. Vérification de l'installation de Python:" && python3 --version

# ---- Télécharger le modèle Mistral ----
RUN wget -O /Lite-Mistral-150M-v2-Instruct-FP16.gguf \
"https://huggingface.co/Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16/resolve/main/Lite-Mistral-150M-v2-Instruct-FP16.gguf?download=true" && \
    echo "Taille du modèle téléchargé:" && du -h /Lite-Mistral-150M-v2-Instruct-FP16.gguf

# ---- Vérification post-téléchargement ----
RUN echo "=== VÉRIFICATION POST-TÉLÉCHARGEMENT ===" && \
    echo "1. Modèle Mistral:" && ls -la /Lite-Mistral-150M-v2-Instruct-FP16.gguf && \
    echo "2. Taille du modèle:" && du -h /Lite-Mistral-150M-v2-Instruct-FP16.gguf

# ---- Créer un environnement virtuel et installer les dépendances ----
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt && \
    echo "Dépendances Python installées:" && pip freeze

# ---- Rendre le script start.sh exécutable ----
RUN chmod +x start.sh

# ---- Vérification finale ----
RUN echo "=== VÉRIFICATION FINALE ===" && \
    echo "1. Environnement virtuel:" && ls -la /venv/bin && \
    echo "2. Exécution de start.sh:" && head -n 5 start.sh

# ---- Exposer le port ----
EXPOSE 8080

# ---- Commande de lancement ----
CMD ["./start.sh"]
