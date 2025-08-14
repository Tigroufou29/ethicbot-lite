FROM debian:bookworm-slim

# Installer dépendances
RUN apt-get update && apt-get install -y \
    git build-essential python3 python3-pip wget curl \
    && rm -rf /var/lib/apt/lists/*

# Cloner et compiler llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp.git
WORKDIR /llama.cpp
RUN make

# Copier le modèle
COPY Lite-Mistral-150M-v2-Instruct-FP16.gguf /Lite-Mistral-150M-v2-Instruct-FP16.gguf

# Copier le serveur Flask
WORKDIR /
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY start.sh .
RUN chmod +x start.sh

# Port par défaut
EXPOSE 8080

CMD ["./start.sh"]
