# app.py
from flask import Flask, request, render_template, jsonify, redirect
from werkzeug.utils import secure_filename
import os
import subprocess
from rag_chain import generate_answer

app = Flask(__name__)
UPLOAD_FOLDER = "/home/cdsw/knowledge_based/document/"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        # Run document ingestion and embedding
        subprocess.run(["python3", "src/ingest.py"])
        subprocess.run(["python3", "src/embed.py"])
    return redirect("/")

@app.route("/chat", methods=["POST"])
def chat():
    query = request.json["query"]
    answer, doc = generate_answer(query)
    image_url = "https://via.placeholder.com/80x60.png?text=" + doc[:10]
    return jsonify({"answer": answer, "image": image_url})

# Start the app in CML environment
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ["CDSW_APP_PORT"]))