import os
import base64
import requests
from flask import Flask, request

app = Flask(__name__)

DESTINATION_SERVER_URL = "https://ef23-103-189-201-6.ngrok-free.app/upload"

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json.get("image")
    if not data:
        return "No image received", 400

    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(DESTINATION_SERVER_URL, json={"image": data}, headers=headers)

        return "Image forwarded!" if response.status_code == 200 else f"Error: {response.status_code}", response.status_code

    except requests.exceptions.RequestException as e:
        return f"Connection error: {e}", 500
    except Exception as e:
        return f"Processing error: {e}", 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)