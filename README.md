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
├── document/                   # 📥 Uploaded PDF files
├── data/                       # 📄 Extracted .txt documents (processed from PDF)
├── embeddings/                 # 🧠 FAISS index and chunk metadata (.faiss, .npy)
│
├── src/                        # 🧪 Core logic and backend components
│   ├── app.py                  # 🔌 Flask web server for chat and upload endpoints
│   ├── ingest.py               # 📤 Extracts text from PDF into structured plain text
│   ├── embed.py               # 🔎 Embeds chunks with SentenceTransformer and stores in FAISS
│   ├── index.py                # 🎯 FAISS search wrapper for semantic retrieval
│   ├── rag_chain.py            # 🧠 Prompt construction and LLM generation (Falcon-7B)
│
├── templates/
│   └── index.html              # 💬 Frontend chat interface (HTML + JS)
│
├── static/
│   ├── style.css               # 🎨 UI styles (light/dark mode, layout, theming)
│   ├── logo.png                # 📛 Project logo for header bar
│   └── chatbot.png             # 🤖 Chatbot avatar shown in answers
│
├── requirements.txt            # 📦 Python dependencies
└── README.md                   # 📘 Project overview and instructions

---

## 🚀 How to Use

### 1. Store PDF Document on /document
### 2. Run Python ingest.py
### 3. Run Python embed.py
### 4. deploy app.py on CML