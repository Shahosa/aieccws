
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
import random
import subprocess
import time

app = FastAPI()
documents = []
start_time = time.time()

fun_prompts = [
    "Write a Terraform plan to colonize Mars.",
    "Generate a Kubernetes manifest for a Hogwarts app.",
    "Summarize logs from a pizza delivery drone network."
]

class QueryRequest(BaseModel):
    prompt: str

class EmbedRequest(BaseModel):
    content: str

@app.post("/embed")
async def embed_text(req: EmbedRequest):
    documents.append(req.content)
    return {"message": "Document embedded successfully", "total_documents": len(documents)}

@app.post("/query")
async def query_model(req: QueryRequest):
    context = "\n".join(documents[-3:])
    return {
        "prompt": req.prompt,
        "context_used": context,
        "response": f"[LLM Answer based on context and prompt: '{req.prompt}']"
    }

@app.get("/fun-prompt")
async def get_fun_prompt():
    return {"prompt": random.choice(fun_prompts)}

@app.get("/status")
def status_check():
    try:
        model_check = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        models = model_check.stdout
        model_loaded = "mistral" in models

        uptime = time.time() - start_time

        return {
            "ollama_model": "mistral",
            "ollama_ready": model_loaded,
            "embedding_loaded": len(documents) > 0,
            "documents_indexed": len(documents),
            "uptime_seconds": round(uptime, 2)
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
