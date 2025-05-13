# ingest.py
import os
import pdfplumber
from pathlib import Path

INPUT_DIR = "/home/cdsw/knowledge_based/document/"
OUTPUT_DIR = "/home/cdsw/knowledge_based/data/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_text_from_pdf(pdf_path):
    """
    Extracts text from a PDF with proper spacing and formatting.
    """
    full_text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            lines = page.extract_text().split('\n') if page.extract_text() else []
            for line in lines:
                # Fix spacing issues like missing spaces between words
                cleaned_line = ' '.join(line.strip().split())
                full_text.append(cleaned_line)
    return '\n'.join(full_text)

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
        os.remove(file)
        print(f"✅ Saved to: {output_file.name}")

if __name__ == "__main__":
    ingest()