import json
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os

class Retriever:
    def __init__(self, index_path=None, meta_path=None, model_name=None):
        model_name = model_name or os.environ.get("MODEL_NAME", "all-MiniLM-L6-v2")
        self.model = SentenceTransformer(model_name)
        self.index = None
        if index_path and os.path.exists(index_path):
            self.index = faiss.read_index(index_path)
        if meta_path and os.path.exists(meta_path):
            with open(meta_path, 'r') as f:
                self.meta = json.load(f)
        else:
            self.meta = []

    def retrieve(self, query, top_k=1):
        if self.index is None:
            return []
        q_emb = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(q_emb)
        D, I = self.index.search(q_emb, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx == -1:
                continue
            results.append({"score": float(score), "doc": self.meta[idx]})
        return results
