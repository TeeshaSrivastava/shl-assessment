import json
import numpy as np
import faiss
import os
from sentence_transformers import SentenceTransformer

DATA_PATH = "data/assessments_clean.json"
INDEX_PATH = "embeddings/faiss.index"
META_PATH = "embeddings/metadata.json"

def build_embeddings():
    print("Building embeddings...")

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        assessments = json.load(f)

    texts = [
        f"{a.get('name','')} {a.get('description','')} {' '.join(a.get('test_type', []))}"
        for a in assessments
    ]

    model = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = model.encode(texts, show_progress_bar=True).astype("float32")

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    os.makedirs("embeddings", exist_ok=True)
    faiss.write_index(index, INDEX_PATH)

    with open(META_PATH, "w", encoding="utf-8") as f:
        json.dump(assessments, f, indent=2)

    print("Embeddings & metadata created")

if __name__ == "__main__":
    build_embeddings()
