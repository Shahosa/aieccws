
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()

# In-memory placeholder for documents and fun prompts
documents = []
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
    context = "\n".join(documents[-3:])  # Use last few documents as dummy context
    return {
        "prompt": req.prompt,
        "context_used": context,
        "response": f"[LLM Answer based on context and prompt: '{req.prompt}']"
    }

@app.get("/fun-prompt")
async def get_fun_prompt():
    return {"prompt": random.choice(fun_prompts)}
