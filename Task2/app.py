from flask import Flask, request
import os

app = Flask(__name__)

keys = []
if os.path.exists(".env"):
    line = open(".env").read().strip()
    line = line.replace("API_KEYS=", "")
    keys = line.split(",")

@app.route("/process", methods=['POST'])
def process():
    key = request.headers.get("X-API-Key")
    if not key:
        return {"error": "Missing API key"}, 401
    if key not in keys:
        return {"error": "Invalid API key"}, 403
    data = request.get_json()
    text = data.get("text")
    if not text:
        return {"error": "Text is required"}, 400
    result = text.upper()
    return {"original": text, "processed": result}

if __name__ == "__main__":
    app.run(host="localhost", port=5000, debug=True)
