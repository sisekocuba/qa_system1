# backend/retriever.py
import json
import os
import numpy as np
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, embeddings_path=None, meta_path=None, model_name=None):
        model_name = model_name or os.environ.get("MODEL_NAME", "all-MiniLM-L6-v2")
        self.model = SentenceTransformer(model_name)
        self.embeddings = None
        self.meta = []
        if embeddings_path and os.path.exists(embeddings_path):
            self.embeddings = np.load(embeddings_path)
        if meta_path and os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                self.meta = json.load(f)

    def retrieve(self, query, top_k=1):
        if self.embeddings is None or len(self.meta) == 0:
            return []
        q_emb = self.model.encode([query], convert_to_numpy=True)
        q_emb = q_emb / (np.linalg.norm(q_emb, axis=1, keepdims=True) + 1e-12)
        # cosine similarity via dot product since vectors are normalized
        scores = (self.embeddings @ q_emb[0]).astype(float)
        idx = np.argsort(-scores)[:top_k]
        results = []
        for i in idx:
            results.append({"score": float(scores[i]), "doc": self.meta[i]})
        return results
