import os
import sys
from flask import Flask, request, render_template, jsonify, redirect
from werkzeug.utils import secure_filename

# Explicitly add src folder to path
sys.path.append("/home/cdsw/knowledge_based/src")

from rag_chain import generate_answer

UPLOAD_FOLDER = "/home/cdsw/knowledge_based/document/"
TEMPLATE_FOLDER = "/home/cdsw/knowledge_based/templates/"
STATIC_FOLDER = "/home/cdsw/knowledge_based/static/"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Tell Flask where to find templates and static files
app = Flask(
    __name__,
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATIC_FOLDER
)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():
    file = request.files.get("file")
    if file:
        filename = secure_filename(file.filename)
        save_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(save_path)

        # Run ingestion and embedding scripts
        os.system("python3 /home/cdsw/knowledge_based/src/ingest.py")
        os.system("python3 /home/cdsw/knowledge_based/src/embed.py")

    return redirect("/")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "")
    if not query.strip():
        return jsonify({"answer": "Please enter a valid question.", "image": ""})

    answer, doc = generate_answer(query)
    image_url = "/static/chatbot.png"  # ← Use your chatbot image here

    return jsonify({
        "answer": answer,
        "image": image_url
    })


# === Run in CML ===
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ["CDSW_APP_PORT"]))