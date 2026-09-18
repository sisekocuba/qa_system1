# Reproduce

1. Create virtualenv and install:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Seed the index:
   python scripts/seed.py

3. Run the API:
   uvicorn backend.main:app --reload --port 8000

4. Test:
   curl "http://127.0.0.1:8000/health"
   curl "http://127.0.0.1:8000/ask?q=Tell+me+about+MedAI"
