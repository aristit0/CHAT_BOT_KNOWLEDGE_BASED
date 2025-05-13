import mlflow
from sentence_transformers import SentenceTransformer
from datetime import datetime

model_name = "all-MiniLM-L6-v2"
documents = [...]  # loaded and preprocessed

mlflow.set_experiment("genai_doc_embedding")

with mlflow.start_run(run_name=f"embedding_run_{datetime.now()}"):
    mlflow.log_param("model_name", model_name)
    model = SentenceTransformer(model_name)
    embeddings = model.encode(documents, show_progress_bar=True)
    mlflow.log_metric("num_documents", len(documents))
    mlflow.log_artifact("your_text_file.txt")  # optional: log cleaned data