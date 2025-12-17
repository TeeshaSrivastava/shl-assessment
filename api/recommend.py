import json
import numpy as np
import faiss
from fastapi import FastAPI
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("embeddings/faiss.index")

# Load metadata
with open("embeddings/metadata.json", "r", encoding="utf-8") as f:
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
                "description": m.get("description", "Assessment aligned to role requirements."),
                "test_type": m.get("test_type", [])
            })

    return {
        "recommended_assessments": results
    }

