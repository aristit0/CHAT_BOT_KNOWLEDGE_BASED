# embed.py
import os
import mlflow
import faiss
import numpy as np
from datetime import datetime
from sentence_transformers import SentenceTransformer

DATA_DIR = "/home/cdsw/knowledge_based/data/"
EMBED_DIR = "/home/cdsw/knowledge_based/embeddings/"
os.makedirs(EMBED_DIR, exist_ok=True)

model_name = "all-MiniLM-L6-v2"
model = SentenceTransformer(model_name, device="cuda")

documents = []
doc_names = []

# Load all .txt files
for fname in os.listdir(DATA_DIR):
    if fname.endswith(".txt"):
        path = os.path.join(DATA_DIR, fname)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read()
            documents.append(text)
            doc_names.append(fname)

# Skip if no documents
if not documents:
    print("⚠️ No documents found to embed.")
    exit()

# Start MLflow logging
mlflow.set_experiment("genai_doc_embedding")

with mlflow.start_run(run_name=f"embedding_run_{datetime.now()}"):
    mlflow.log_param("model_name", model_name)
    mlflow.log_metric("num_documents", len(documents))

    embeddings = model.encode(documents, show_progress_bar=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save index and document names
    index_path = os.path.join(EMBED_DIR, "index.faiss")
    names_path = os.path.join(EMBED_DIR, "names.npy")
    faiss.write_index(index, index_path)
    np.save(names_path, np.array(doc_names))

    mlflow.log_artifact(index_path)
    mlflow.log_artifact(names_path)

    print(f"✅ Embedded {len(documents)} documents")