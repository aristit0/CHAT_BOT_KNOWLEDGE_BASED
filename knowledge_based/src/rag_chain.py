# rag_chain.py
from transformers import pipeline
from index import search
import os

# Load LLM pipeline with GPU
MODEL = pipeline(
    "text-generation",
    model="tiiuae/falcon-7b-instruct",
    trust_remote_code=True,
    device=0  # GPU ID
)

DATA_DIR = "/home/cdsw/knowledge_based/data/"

def generate_answer(query):
    """
    Retrieve relevant documents and use Falcon-7B to generate a response.

    Args:
        query (str): The user’s troubleshooting question.

    Returns:
        Tuple (answer, document filename)
    """
    # Step 1: Retrieve most relevant docs
    top_docs = search(query)

    # Step 2: Read and truncate content from top doc(s)
    context = "\n---\n".join(
        open(os.path.join(DATA_DIR, fname), encoding="utf-8").read()[:1000]
        for fname in top_docs
    )

    # Step 3: Build prompt for LLM
    prompt = f"""You are a helpful assistant for IT troubleshooting.
Context:
{context}

Question: {query}
Answer:"""

    # Step 4: Generate output from LLM
    output = MODEL(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
    result = output[0]["generated_text"].split("Answer:")[-1].strip()

    return result, top_docs[0] if top_docs else ""