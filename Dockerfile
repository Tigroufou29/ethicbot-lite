FROM debian:bookworm-slim

# Installer dépendances
RUN apt-get update && apt-get install -y \
    git curl python3 python3-pip && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Installer llama.cpp server
RUN git clone https://github.com/ggerganov/llama.cpp.git /app/llama.cpp && \
    cd /app/llama.cpp && make -j && \
    pip install flask

# Copier le script API
COPY app.py /app/
COPY start.sh /app/
RUN chmod +x /app/start.sh

# Lancer le serveur
WORKDIR /app
CMD ["./start.sh"]
