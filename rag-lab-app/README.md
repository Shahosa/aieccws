# 🧠 RAG Lab - Generative AI Demo App

This project is a lightweight Retrieval-Augmented Generation (RAG) API designed for workshops and learning sessions. It uses [Ollama](https://ollama.com/) to run local language models and FastAPI to serve a fully interactive, secure backend.

---

## 🚀 Features

- 📄 Upload plain text documents (`/upload`)
- 🧠 Query a local LLM with or without context (`/query`)
- 💬 Embed notes or snippets directly (`/embed`)
- 📜 Fun break prompts for creative demos (`/fun-prompt`)
- 🧹 Clear embedded data (`/clear`)
- 🧾 View query history (`/history`)
- 🔐 `x-api-key` security
- 🖥 HTML UI for non-developers
- ✅ Designed for roles like Developer, Architect, PO, Scrum Master

---

## 🛠 Setup Instructions

1. **Launch EC2 with CloudFormation**
   - Use the provided `rag_lab_v4_correct_root.yaml` file
   - Ensure 50GiB root disk and public IP enabled

2. **Access the app**
   - Visit `http://<PublicDNS>` to access the HTML UI
   - Use Postman or curl for raw API interaction

3. **Default API Key**
   - Key: `RAGLAB123`
   - Required for all endpoints except `/status` and `/`

---

## 🔧 API Endpoints

| Endpoint       | Method | Auth Required | Description |
|----------------|--------|----------------|-------------|
| `/status`      | GET    | ❌             | Health check |
| `/upload`      | POST   | ✅             | Upload `.txt` files |
| `/embed`       | POST   | ✅             | Add raw string |
| `/query`       | POST   | ✅             | Ask a question (uses RAG if docs exist) |
| `/clear`       | POST   | ✅             | Clear all uploaded docs |
| `/history?n=5` | GET    | ✅             | Get last N queries |
| `/fun-prompt`  | GET    | ✅             | Random creative prompt |
| `/`            | GET    | ❌             | Launch HTML UI |

---

## 🧪 Prompt Examples

- “Summarize the uploaded document.”
- “What design patterns are mentioned?”
- “List the pros and cons discussed.”
- “What does the doc say about GDPR compliance?”

---

## 💻 Frontend Preview

Open your browser to `/` and:
- Upload `.txt` files
- Choose from example prompts
- Query the model
- Download your response as `.txt`

---

## 📦 File Structure

- `app.py` — Full FastAPI backend
- `rag_lab_ui.html` — UI frontend
- `documents.json` — Auto-generated persistent memory
- `postman_collection.json` — Postman request set
- `rag_lab_v4_correct_root.yaml` — CloudFormation infra

---

## 🧼 Cleanup

To remove the stack, simply delete it via CloudFormation.  
No auto-shutdown is configured — resources persist unless removed.

---

## 👋 Maintainer

Created for interactive workshops and GenAI demos by @shahosa  
https://github.com/Shahosa/aieccws