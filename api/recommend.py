import json
import os
import faiss
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

# 👇 IMPORT THE BUILDER
from embeddings.build_embeddings import build_embeddings

app = FastAPI()

INDEX_PATH = "embeddings/faiss.index"
META_PATH = "embeddings/metadata.json"

# 🔁 AUTO-BUILD EMBEDDINGS IF MISSING
if not os.path.exists(INDEX_PATH) or not os.path.exists(META_PATH):
    print("Embeddings not found. Building now...")
    build_embeddings()

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index(INDEX_PATH)

# Load metadata
with open(META_PATH, "r", encoding="utf-8") as f:
    metadata = json.load(f)


class JobInput(BaseModel):
    job_description: str
    top_k: int = 5


@app.post("/recommend")
def recommend(data: JobInput):
    query_embedding = model.encode([data.job_description]).astype("float32")
    distances, indices = index.search(query_embedding, data.top_k)

    results = []
    for idx in indices[0]:
        if idx < len(metadata):
            m = metadata[idx]
            results.append({
                "name": m.get("name", "Unknown Assessment"),
                "url": m.get("url", ""),
                "description": m.get("description", ""),
                "test_type": m.get("test_type", [])
            })

    return {"recommended_assessments": results}

