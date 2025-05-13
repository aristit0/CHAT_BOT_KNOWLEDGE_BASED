# index.py
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load the SentenceTransformer model on GPU
MODEL = SentenceTransformer("all-MiniLM-L6-v2", device="cuda")

# Load FAISS index and document name list
INDEX = faiss.read_index("/home/cdsw/knowledge_based/embeddings/index.faiss")
DOC_NAMES = np.load("/home/cdsw/knowledge_based/embeddings/names.npy")

def search(query, top_k=3):
    """
    Search the most relevant documents for a given query.

    Args:
        query (str): Natural language question
        top_k (int): Number of top documents to return

    Returns:
        list of str: Filenames of the top documents
    """
    emb = MODEL.encode([query])
    D, I = INDEX.search(emb, top_k)
    return [DOC_NAMES[i] for i in I[0]]