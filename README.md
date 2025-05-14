# GenAI PDF Knowledge Chatbot on Cloudera Machine Learning (CML)

This project is a Retrieval-Augmented Generation (RAG) chatbot designed for IT troubleshooting. It allows you to upload documents (PDF or Google Docs), extract and embed knowledge, and ask natural language questions to receive contextual answers powered by Falcon-7B and FAISS vector search.

---

## 🔧 Features

- 📁 Upload and ingest PDF documents via web UI
- 🧠 Extract structured text and store as `.txt`
- 🔍 Chunk-based embedding using SentenceTransformer (`all-MiniLM-L6-v2`)
- ⚡ Vector similarity search with FAISS
- 🤖 Answer generation with Falcon-7B (`tiiuae/falcon-7b-instruct`) on GPU
- 🌙 Modern dark/light toggle UI with document list and download support
- 📦 MLflow logging for embeddings

---

## 📁 Folder Structure

knowledge_based/
├── document/       # Uploaded PDFs
├── data/           # Processed text files
├── embeddings/     # FAISS index and metadata
├── src/
│   ├── app.py          # Flask web server
│   ├── ingest.py       # Extract PDF -> TXT
│   ├── embed.py        # Embed TXT -> FAISS
│   ├── index.py        # FAISS search logic
│   ├── rag_chain.py    # RAG pipeline with Falcon
├── templates/
│   └── index.html      # Chat UI
├── static/
│   ├── style.css       # UI styling
│   ├── chatbot.png     # Bot avatar
│   └── logo.png        # Logo

---

## 🚀 How to Use

### 1. Store PDF Document on /document
### 2. Run Python ingest.py
### 3. Run Python embed.py
### 4. deploy app.py on CML