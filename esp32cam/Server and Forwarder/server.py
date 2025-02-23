from flask import Flask, request, render_template
import base64
import os

app = Flask(__name__)
UPLOAD_FOLDER = "static"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    data = request.json.get("image")
    if not data:
        return "No image received", 400

   
    img_path = os.path.join(UPLOAD_FOLDER, "esp32cam.jpg")
    with open(img_path, "wb") as img_file:
        img_file.write(base64.b64decode(data))

    return "Gambar diterima!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
