from backend.main import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json().get("status") == "ok"

def test_ask_medai():
    r = client.get("/ask", params={"q":"Tell me about MedAI"})
    assert r.status_code == 200
    assert "MedAI" in r.json().get("answer","") or "diagnostic" in r.json().get("answer","")
