from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import random
import httpx
import os
import json

app = FastAPI()
OLLAMA_MODEL = "gemma:2b"
OLLAMA_HOST = "http://localhost:11434"
API_KEY = "RAGLAB123"
DATA_FILE = "documents.json"
HISTORY_LIMIT = 50
DEFAULT_MODEL = "gemma:2b"
query_history = []
uery_history = []
if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        documents = json.load(f)
else:
    documents = []

fun_prompts =  [
    "Pitch a startup founded by dragons 🐉.",
    "Write Jira tickets for Hogwarts IT.",
    "Debug a coffee machine with attitude problems ☕🤖.",
    "Describe microservices architecture for the Shire 🧝‍♂️.",
    "Generate error messages for a time-traveling toaster.",
    "Design a CI/CD pipeline for a spaceship mission to Mars 🚀.",
    "Draw the architecture diagram of Mordor’s monitoring stack.",
    "Slackbot that refuses to answer HR questions.",
    "Terraform script for castle infrastructure.",
    "Traceback from a dream interpreter's API."
]
class EmbedRequest(BaseModel):
    content: str

class QueryRequest(BaseModel):
    prompt: str

def save_documents():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

@app.middleware("http")
async def api_key_check(request: Request, call_next):
    if request.url.path not in ["/", "/status"]:
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return HTMLResponse("Unauthorized", status_code=401)
    return await call_next(request)

@app.get("/status")
async def status():
    return {
        "ollama_model": DEFAULT_MODEL,
        "ollama_ready": True,
        "embedding_loaded": len(documents) > 0,
        "documents_indexed": len(documents),
        "uptime_seconds": 123.45
    }

@app.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    accepted = 0
    skipped = 0
    for file in files:
        content = await file.read()
        try:
            text = content.decode("utf-8")
            documents.append(text)
            accepted += 1
        except UnicodeDecodeError:
            skipped += 1
    save_documents()
    return {
        "message": "Files uploaded and embedded",
        "documents_indexed": accepted,
        "documents_skipped": skipped
    }

@app.post("/embed")
async def embed_text(req: EmbedRequest):
    documents.append(req.content)
    save_documents()
    return {"message": "Document embedded successfully", "total_documents": len(documents)}

@app.post("/query")
async def query_model(req: QueryRequest):
    if documents:
        context = "\n".join(documents[-3:])
        full_prompt = f"Use the following context:\n{context}\n\nQuestion: {req.prompt}"
    else:
        full_prompt = req.prompt

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={"model": "mistral", "prompt": full_prompt}
            )
            result = response.json()
        answer = result.get("response", "No answer returned")
    except Exception as e:
        answer = f"[Error communicating with Ollama: {str(e)}]"

    entry = {
        "prompt": req.prompt,
        "rag_mode": bool(documents),
        "context_used": context if documents else None,
        "response": answer
    }
    query_history.append(entry)
    if len(query_history) > HISTORY_LIMIT:
        query_history.pop(0)

    return entry

@app.get("/history")
async def get_history(n: int = 10):
    return query_history[-n:]

@app.post("/clear")
async def clear_documents():
    documents.clear()
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    return {"message": "All embedded documents cleared."}

@app.get("/fun-prompt")
async def get_fun_prompt():
    return {"prompt": random.choice(fun_prompts)}

@app.get("/", response_class=HTMLResponse)
async def root_ui():
    with open("rag_lab_ui.html", "r", encoding="utf-8") as f:
        return f.read()