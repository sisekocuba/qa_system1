from fastapi import FastAPI, Query
from backend.retriever import Retriever
from backend.summarizer import Summarizer
import uvicorn
import os

app = FastAPI(title="QA System")

# Paths are relative to repo root when running uvicorn from repo root
INDEX_PATH = os.environ.get("FAISS_INDEX_PATH", "data/embeddings.npy")
META_PATH = os.environ.get("META_PATH", "data/meta.json")

retriever = Retriever(index_path=INDEX_PATH, meta_path=META_PATH)
summarizer = Summarizer()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ask")
def ask(q: str = Query(..., description="User question")):
    hits = retriever.retrieve(q, top_k=1)
    if not hits:
        return {"question": q, "answer": "Sorry, I don't have an answer for that yet."}
    raw = hits[0]["doc"]["text"]
    summary = summarizer.summarize(raw)
    return {"question": q, "answer": summary, "source": hits[0]['doc']['title'], "score": hits[0]['score']}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
