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
RUN wget -O /Lite-Mistral-150M-v2-Instruct-FP16.gguf "https://huggingface.co/Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16/resolve/main/Lite-Mistral-150M-v2-Instruct-FP16.gguf?download=true"

# ---- Installer les dépendances Python ----
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Copier l'application ----
COPY app.py .

# ---- Exposer le port ----
EXPOSE 8080

# ---- Lancer l'application ----
CMD ["python3", "app.py"]
