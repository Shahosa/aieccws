from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List,Optional
import random
import httpx
import os
import json
from  utils import extract_text

app = FastAPI()
DOCUMENTS_PATH = "documents.json"
ALLOWED_EXTENSIONS = {".txt", ".pdf", ".docx"}
documents = []
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
    use_rag: Optional[bool] = True

@app.on_event("startup")
async def load_documents():
    global documents
    if os.path.exists(DOCUMENTS_PATH):
        with open(DOCUMENTS_PATH, "r") as f:
            try:
                documents = json.load(f)
            except json.JSONDecodeError:
                documents = []

def save_documents():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(documents, f, ensure_ascii=False, indent=2)

def extract_text(file: UploadFile) -> str:
    if file.filename.endswith(".pdf"):
        pdf = fitz.open(stream=file.file.read(), filetype="pdf")
        return "\n".join(page.get_text() for page in pdf)
    elif file.filename.endswith(".docx"):
        doc = docx.Document(file.file)
        return "\n".join(p.text for p in doc.paragraphs)
    else:  # Assume text
        return file.file.read().decode("utf-8")
                

@app.middleware("http")
async def api_key_check(request: Request, call_next):
    if request.url.path not in ["/", "/status"]:
        key = request.headers.get("x-api-key")
        if key != API_KEY:
            return HTMLResponse("Unauthorized", status_code=401)
    return await call_next(request)

@app.get("/status")
async def get_status():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post("http://localhost:11434/api/generate", json={"model": "gemma:2b", "prompt": "ping"})
            is_ready = "error" not in response.text.lower()
    except:
        is_ready = False

    return {
        "ollama_model": "gemma:2b",
        "ollama_ready": is_ready,
        "embedding_loaded": bool(documents),
        "documents_indexed": len(documents),
        "uptime_seconds": round(os.times().elapsed, 2)
    }


@app.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    global documents
    indexed, skipped = 0, 0
    for file in files:
        ext = os.path.splitext(file.filename)[1].lower()
        if ext in ALLOWED_EXTENSIONS:
            content = await file.read()
            text = extract_text(ext, content)
            if text.strip():
                documents.append(text.strip())
                indexed += 1
            else:
                skipped += 1
        else:
            skipped += 1

    with open(DOCUMENTS_PATH, "w") as f:
        json.dump(documents, f)
    return {"message": "Files uploaded and embedded", "documents_indexed": indexed, "documents_skipped": skipped}


@app.post("/embed")
async def embed_text(req: EmbedRequest):
    documents.append(req.content)
    save_documents()
    return {"message": "Document embedded successfully", "total_documents": len(documents)}

class QueryRequest(BaseModel):
    prompt: str
    use_rag: Optional[bool] = True

@app.post("/query")
async def query_model(req: QueryRequest):
    if req.use_rag and documents:
        context = "\n".join(documents[-3:])
        full_prompt = f"Use the following context:\n{context}\n\nQuestion: {req.prompt}"
    else:
        context = None
        full_prompt = req.prompt

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/generate",
                json={"model": "gemma:2b", "prompt": full_prompt}
            )
            result = response.json()
        answer = result.get("response", "No answer returned")
    except Exception as e:
        answer = f"[Error communicating with Ollama: {str(e)}]"

    entry = {
        "prompt": req.prompt,
        "rag_mode": req.use_rag and bool(documents),
        "context_used": context,
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
    global documents
    documents = []
    if os.path.exists(DOCUMENTS_PATH):
        os.remove(DOCUMENTS_PATH)
    return {"message": "Documents cleared."}

@app.get("/fun-prompt")
async def get_fun_prompt():
    return {"prompt": random.choice(fun_prompts)}

@app.get("/", response_class=HTMLResponse)
async def root_ui():
    with open("rag_lab_ui.html", "r", encoding="utf-8") as f:
        return f.read()