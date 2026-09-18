import json, os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

docs = [
  {"id":"doc_1","title":"Company Overview","text":"Our company specializes in AI-driven solutions for healthcare and finance. Founded in 2015, offices in Cape Town and Johannesburg."},
  {"id":"doc_2","title":"Product Info","text":"MedAI is a diagnostic support tool that reduces diagnostic errors by 20%."},
  {"id":"doc_3","title":"Employee Policy","text":"Employees are entitled to 20 days of annual leave. Remote work is supported with approval from management. All staff must complete cybersecurity training annually."}
]

os.makedirs("data", exist_ok=True)
with open("data/meta.json","w") as f:
    json.dump(docs, f, indent=2)

model = SentenceTransformer(os.environ.get("MODEL_NAME","all-MiniLM-L6-v2"))
texts = [d["text"] for d in docs]
emb = model.encode(texts, convert_to_numpy=True)
faiss.normalize_L2(emb)
d = emb.shape[1]
index = faiss.IndexFlatIP(d)
index.add(emb)
faiss.write_index(index, "data/faiss.index")
print("Seed complete: data/meta.json and data/faiss.index created.")
