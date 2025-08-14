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
COPY . .

# ---- Vérifications critiques ----
RUN echo "=== VÉRIFICATION DES FICHIERS ===" && \
    echo "1. Fichiers à la racine:" && ls -la && \
    echo "2. Contenu du dossier templates:" && ls -la /templates && \
    echo "3. Contenu complet de app.py:" && cat app.py && \
    echo "4. Exécutable llama.cpp:" && ls -la /llama.cpp/build/bin/main && \
    echo "5. Vérification de l'installation de Python:" && python3 --version

# ---- Télécharger le modèle Mistral ----
RUN wget -O /Lite-Mistral-150M-v2-Instruct-FP16.gguf \
"https://huggingface.co/Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16/resolve/main/Lite-Mistral-150M-v2-Instruct-FP16.gguf?download=true"

# ---- Créer un environnement virtuel et installer les dépendances ----
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ---- Rendre le script start.sh exécutable ----
RUN chmod +x start.sh

# ---- Exposer le port ----
EXPOSE 8080

# ---- Commande de lancement avec logging ----
CMD ["sh", "-c", "python3 app.py >> /var/log/app.log 2>&1"]
