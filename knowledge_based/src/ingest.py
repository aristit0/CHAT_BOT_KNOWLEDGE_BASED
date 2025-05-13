# ingest.py
import os
import pdfplumber
from pathlib import Path

INPUT_DIR = "/home/cdsw/knowledge_based/document/"
OUTPUT_DIR = "/home/cdsw/knowledge_based/data/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join(page.extract_text() or "" for page in pdf.pages)

def ingest():
    pdf_files = list(Path(INPUT_DIR).glob("*.pdf"))
    if not pdf_files:
        print("⚠️ No PDF files found in input folder.")
        return

    for file in pdf_files:
        print(f"📄 Processing: {file.name}")
        text = extract_text_from_pdf(file)
        output_file = Path(OUTPUT_DIR) / (file.stem + ".txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        os.remove(file)  # Cleanup
        print(f"✅ Saved to: {output_file.name}")

if __name__ == "__main__":
    ingest()