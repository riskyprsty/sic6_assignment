from flask import Flask, request, render_template
import base64
import os
import pymongo # meng-import library pymongo yang sudah kita install

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://UNI022:UNI022@cluster0.ac7up.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client["UNI022"]
collection = db["assignment_2"]


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

@app.route("/insert_data", methods=["POST"])
def insert_data():
    try:
        data = request.json
        collection.insert_many(data)
        return "Data berhasil dimasukkan ke database", 200
    except Exception as e:
        return str(e), 400



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)