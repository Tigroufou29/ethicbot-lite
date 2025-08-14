import subprocess
import os
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

MODEL_PATH = "/Lite-Mistral-150M-v2-Instruct-FP16.gguf"
LLAMA_CPP_DIR = "/llama.cpp"
LLAMA_CPP_EXECUTABLE = os.path.join(LLAMA_CPP_DIR, "build", "bin", "main")

@app.route("/v1/chat/completions", methods=["POST"])
def chat_completions():
    data = request.json
    messages = data.get("messages", [])
    
    # Construire le prompt à partir des messages
    prompt = ""
    for msg in messages:
        prompt += f"{msg['role']}: {msg['content']}\n"
    prompt += "assistant:"
    
    cmd = [
        LLAMA_CPP_EXECUTABLE,
        "-m", MODEL_PATH,
        "-p", prompt,
        "-n", "200",
        "--temp", "0.7",
        "--ctx-size", "2048"
    ]
    
    try:
        output = subprocess.check_output(cmd, universal_newlines=True)
        # Extraire uniquement la réponse de l'assistant
        response = output.split("assistant:")[-1].strip()
        
        return jsonify({
            "choices": [{
                "message": {
                    "role": "assistant",
                    "content": response
                }
            }]
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/chat")
def chat_interface():
    return render_template("chat.html")

@app.route("/")
def home():
    return "Lite Mistral API OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
