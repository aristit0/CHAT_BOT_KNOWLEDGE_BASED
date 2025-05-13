import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model
MODEL = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")

# Load FAISS index and chunk reference names
INDEX = faiss.read_index("/home/cdsw/knowledge_based/embeddings/index.faiss")
CHUNK_NAMES = np.load("/home/cdsw/knowledge_based/embeddings/names.npy", allow_pickle=True)

# Load chunk content (optional, if stored externally)
CHUNK_MAP = {}

DATA_DIR = "/home/cdsw/knowledge_based/data/"
for fname in set(name.split("::")[0] for name in CHUNK_NAMES):
    with open(DATA_DIR + fname, "r", encoding="utf-8") as f:
        sections = f.read().split("\n\n")
        for i, chunk in enumerate(sections):
            CHUNK_MAP[f"{fname}::chunk{i}"] = chunk.strip()

def search(query, top_k=3):
    """
    Search top-k relevant content chunks from embedded knowledge base.
    Returns: List of tuples (chunk_text, chunk_id)
    """
    emb = MODEL.encode([query])
    D, I = INDEX.search(emb, top_k)
    
    results = []
    for idx in I[0]:
        chunk_id = CHUNK_NAMES[idx]
        chunk_text = CHUNK_MAP.get(chunk_id, "[Missing chunk]")
        results.append((chunk_text, chunk_id))

    return results