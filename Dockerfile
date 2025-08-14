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

# ---- Télécharger ton modèle Hugging Face ----
WORKDIR /
RUN wget -O /Lite-Mistral-150M-v2-Instruct-FP16.gguf "https://huggingface.co/Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16/resolve/main/Lite-Mistral-150M-v2-Instruct-FP16.gguf?download=true"

# ---- Installer Python + Flask ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copier ton API ----
COPY app.py .
COPY start .

# ---- Exposer le port ----
EXPOSE 8080

# ---- Commande de démarrage ----
CMD ["bash", "start"]
