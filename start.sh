#!/bin/bash
set -e

# Télécharger le modèle Hugging Face (Lite Mistral)
MODEL_URL="https://huggingface.co/Philtonslip/Lite-Mistral-150M-v2-Instruct-FP16/resolve/main/Lite-Mistral-150M-v2-Instruct-FP16.gguf"
MODEL_FILE="/app/model.gguf"

if [ ! -f "$MODEL_FILE" ]; then
    echo "Téléchargement du modèle..."
    curl -L "$MODEL_URL" -o "$MODEL_FILE"
fi

# Lancer llama.cpp server avec le modèle
./llama.cpp/server -m "$MODEL_FILE" -c 2048 --port 8080
