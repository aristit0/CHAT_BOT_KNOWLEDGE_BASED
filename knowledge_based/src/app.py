import os
import sys
from flask import Flask, request, render_template, jsonify, redirect
from werkzeug.utils import secure_filename

# Ensure the current script can access other modules in /src
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rag_chain import generate_answer

app = Flask(__name__)
UPLOAD_FOLDER = "/home/cdsw/knowledge_based/document/"
TEMPLATE_FOLDER = "/home/cdsw/knowledge_based/templates/"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Set the template folder explicitly
app.template_folder = TEMPLATE_FOLDER


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

        # Run document ingestion and embedding pipeline
        os.system("python3 /home/cdsw/knowledge_based/src/ingest.py")
        os.system("python3 /home/cdsw/knowledge_based/src/embed.py")

    return redirect("/")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    query = data.get("query", "")
    if not query.strip():
        return jsonify({"answer": "Please enter a valid question.", "image": ""})

    # Generate the LLM response and retrieve source document
    answer, doc = generate_answer(query)

    # Create a dummy preview image (you can replace this with something real)
    image_url = "https://via.placeholder.com/80x60.png?text=" + doc[:10]

    return jsonify({
        "answer": answer,
        "image": image_url
    })


# === Run in CML ===
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ["CDSW_APP_PORT"]))