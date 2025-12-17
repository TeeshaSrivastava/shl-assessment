import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
import os

DATA_PATH = "data/assessments_clean.json"
INDEX_PATH = "embeddings/faiss.index"
META_PATH = "embeddings/metadata.json"

# Load data
with open(DATA_PATH, "r", encoding="utf-8") as f:
    assessments = json.load(f)

print(f"Loaded {len(assessments)} assessments")

# Prepare text for embedding
texts = []
for a in assessments:
    combined = f"{a.get('name', '')}. {a.get('description', '')}. {' '.join(a.get('test_type', []))}"
    texts.append(combined)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Generate embeddings
print("Generating embeddings...")
embeddings = model.encode(texts, show_progress_bar=True)

embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# Save index and metadata
faiss.write_index(index, INDEX_PATH)

with open(META_PATH, "w", encoding="utf-8") as f:
    json.dump(assessments, f, indent=2)

print("FAISS index built successfully")
print(f"Index size: {index.ntotal}")
