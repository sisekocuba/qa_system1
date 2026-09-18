# scripts/seed.py
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

# Example documents; replace or extend as needed
docs = [
  {"id":"doc_1","title":"Company Overview","text":"Our company specializes in AI-driven solutions for healthcare and finance. Founded in 2015, offices in Cape Town and Johannesburg."},
  {"id":"doc_2","title":"Product Info","text":"MedAI is a diagnostic support tool that reduces diagnostic errors by 20%."},
  {"id":"doc_3","title":"Employee Policy","text":"Employees are entitled to 20 days of annual leave. Remote work is supported with approval from management. All staff must complete cybersecurity training annually."}
]

os.makedirs("data", exist_ok=True)

# Save meta.json
with open("data/meta.json","w") as f:
    json.dump(docs, f, indent=2)

# Compute embeddings
model_name = os.environ.get("MODEL_NAME", "all-MiniLM-L6-v2")
model = SentenceTransformer(model_name)

texts = [d["text"] for d in docs]
emb = model.encode(texts, convert_to_numpy=True)
# Normalize embeddings for cosine similarity
norms = np.linalg.norm(emb, axis=1, keepdims=True)
emb = emb / (norms + 1e-12)

# Save embeddings
np.save("data/embeddings.npy", emb)
print("Seed complete: data/meta.json and data/embeddings.npy created.")
