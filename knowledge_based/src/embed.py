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

chunks = []
chunk_sources = []

# Load and split each .txt file by section or paragraph
for fname in os.listdir(DATA_DIR):
    if not fname.endswith(".txt"):
        continue

    path = os.path.join(DATA_DIR, fname)
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
        sections = content.split("\n\n")  # Split by empty line (paragraph separator)

        for i, section in enumerate(sections):
            clean = section.strip()
            if len(clean) > 30:  # Avoid tiny chunks
                chunks.append(clean)
                chunk_sources.append(f"{fname}::chunk{i}")

# Skip if no chunks
if not chunks:
    print("⚠️ No text chunks found.")
    exit()

# MLflow experiment
mlflow.set_experiment("genai_doc_embedding")

with mlflow.start_run(run_name=f"chunked_embedding_{datetime.now()}"):
    mlflow.log_param("model_name", model_name)
    mlflow.log_metric("num_chunks", len(chunks))

    embeddings = model.encode(chunks, show_progress_bar=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    # Save index and sources
    index_path = os.path.join(EMBED_DIR, "index.faiss")
    names_path = os.path.join(EMBED_DIR, "names.npy")
    faiss.write_index(index, index_path)
    np.save(names_path, np.array(chunk_sources))

    mlflow.log_artifact(index_path)
    mlflow.log_artifact(names_path)

    print(f"✅ Embedded {len(chunks)} text chunks")