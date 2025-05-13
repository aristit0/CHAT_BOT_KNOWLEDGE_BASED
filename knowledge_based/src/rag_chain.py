import sys
import os

# Ensure index.py is found if in a separate folder
sys.path.append("/home/cdsw/knowledge_based/src")
from index import search

from transformers import pipeline

# Load Falcon model with GPU
MODEL = pipeline(
    "text-generation",
    model="tiiuae/falcon-7b-instruct",
    trust_remote_code=True,
    device=0  # Use GPU 0
)

def generate_answer(query):
    """
    Generate answer using retrieved text chunks and Falcon-7B.
    Returns: (answer_text, source_chunk_name)
    """
    # Step 1: Retrieve top matching chunks (text, chunk_id)
    top_chunks = search(query)

    if not top_chunks:
        return "Sorry, I couldn't find anything relevant in your documents.", ""

    # Step 2: Assemble prompt context from chunks
    context = "\n---\n".join(chunk[0] for chunk in top_chunks)

    prompt = f"""You are a helpful assistant for IT troubleshooting.

Context:
{context}

Question: {query}
Answer:"""

    # Step 3: Run Falcon to generate the response
    output = MODEL(prompt, max_new_tokens=200, do_sample=True, temperature=0.7)
    result = output[0]["generated_text"].split("Answer:")[-1].strip()

    # Step 4: Return the result and source chunk ID
    return result, top_chunks[0][1]