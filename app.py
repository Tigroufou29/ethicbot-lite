import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

MODEL_PATH = "Lite-Mistral-150M-v2-Instruct-FP16.gguf"

@app.route("/chat", methods=["POST"])
def chat():
    prompt = request.json.get("prompt", "")
    cmd = [
        "./llama.cpp/main",
        "-m", MODEL_PATH,
        "-p", prompt,
        "-n", "200"
    ]
    try:
        output = subprocess.check_output(cmd, universal_newlines=True)
        return jsonify({"response": output})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "Lite Mistral API OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
