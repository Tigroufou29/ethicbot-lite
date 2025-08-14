# ---- Base image ----
FROM debian:bookworm-slim

# ---- Installer les dépendances ----
RUN apt-get update && apt-get install -y \
    git build-essential python3 python3-pip wget curl \
    && rm -rf /var/lib/apt/lists/*

# ---- Cloner et compiler llama.cpp ----
RUN git clone https://github.com/ggerganov/llama.cpp.git /llama.cpp
WORKDIR /llama.cpp
RUN make

# ---- Télécharger le modèle directement ----
WORKDIR /
RUN wget -O /Lite-Mistral-150M-v2-Instruct-FP16.gguf "LIEN_DIRECT_VERS_LE_MODELE"

# ---- Copier le serveur Flask ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY start .

# ---- Exposer le port ----
EXPOSE 8080

# ---- Lancer l'application ----
CMD ["bash", "start"]
