
# RAG Lab App

A simple FastAPI-based backend for running Retrieval-Augmented Generation (RAG) labs with Ollama and Postman.

## 🚀 Features
- `/embed`: Upload and store document content (simulates embedding)
- `/query`: Send a prompt and receive a context-aware response
- `/fun-prompt`: Returns a random funny GenAI prompt

## 🧱 Prerequisites
- Python 3.8+
- Ollama running locally (model pulled, e.g., `mistral`)
- pip-installed dependencies: `pip install -r requirements.txt`

## ▶️ Run Locally
```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 📬 Endpoints
### `POST /embed`
```json
{
  "content": "Your document or markdown text here."
}
```

### `POST /query`
```json
{
  "prompt": "What are the onboarding steps?"
}
```

### `GET /fun-prompt`
Returns a fun or humorous GenAI prompt.

## 📁 Example Document
See `sample.md` for a test upload.

---

Created for GenAI Workshop Lab 2 — by Shaho Sadeghi
