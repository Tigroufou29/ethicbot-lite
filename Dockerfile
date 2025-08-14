# ---- Base ----
FROM debian:bookworm-slim

# ---- Installer les dépendances ----
RUN apt-get update && apt-get install -y \
    git build-essential python3 python3-pip wget curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Cloner llama.cpp ----
RUN git clone https://github.com/ggerganov/llama.cpp.git /llama.cpp
WORKDIR /llama.cpp
RUN make

# ---- Copier les fichiers de l'application ----
WORKDIR /
COPY app.py .
COPY requirements.txt .
COPY start.sh .  # Fonctionnera maintenant que start.sh est dans le repo

# ---- Télécharger le modèle Mistral ----
RUN wget -O /Lite-Mistral-150M-v2-Instruct-FP16.gguf \
"https://huggingface.co/Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16/resolve/main/Lite-Mistral-150M-v2-Instruct-FP16.gguf?download=true"

# ---- Installer les dépendances Python ----
RUN pip install --no-cache-dir -r requirements.txt

# ---- Rendre le script start.sh exécutable ----
RUN chmod +x start.sh  # Important pour l'exécution

# ---- Exposer le port ----
EXPOSE 8080

# ---- Commande de lancement ----
CMD ["./start.sh"]
