from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from typing import List
import random

app = FastAPI()
documents = []

fun_prompts = ['Pitch a startup founded by dragons 🐉.', 'Write Jira tickets for Hogwarts IT.', 'Debug a coffee machine with attitude problems ☕🤖.', 'Describe microservices architecture for the Shire 🧝\u200d♂️.', 'Generate error messages for a time-traveling toaster.', 'Design a CI/CD pipeline for a spaceship mission to Mars 🚀.', "Write an RFC to rename '404 Not Found' to 'Lost in the Sauce'.", 'Draft a GDPR policy for Atlantis 🐠.', 'Write test cases for a broomstick ride-sharing app.', 'DevOps checklist for taming a Hydra in Kubernetes 🐍.', 'Draw the architecture diagram of Mordor’s monitoring stack.', 'Code review feedback for an AI that speaks only Shakespearean.', 'Slack conversation between two AI assistants planning a coup.', 'Uptime report for the Batcave infrastructure 🦇.', 'Explain prompt injection to a medieval knight.', 'Write a data breach apology from Jurassic Park 🦖.', 'Deploy a serverless backend for a magic wand API.', 'Refactor the user journey of a haunted house website 👻.', 'Model hallucinations explained to a ghost.', 'Error message from a telepathic LLM.', 'Design sprint for a wizard e-commerce store.', 'Agile retrospective run by sentient vending machines.', 'Chat transcript between two pizza delivery drones.', 'Incident report from a time-travel paradox bug.', 'Toastmasters speech by a robot learning sarcasm.', 'Generate OKRs for a unicorn AI startup.', 'Dockerfile for a potion brewing microservice 🧪.', 'API contract for a sarcasm-as-a-service platform.', 'Debugging notes from a confused LLM trained on memes.', 'PagerDuty alert triggered by ghost activity.', 'Database schema for a zombie dating app.', 'Logging strategy for dreams harvested in the cloud.', 'An agile coach mentoring elves in a forest project.', 'Marketing copy for a sentient shoe.', 'Email auto-reply from a workaholic chatbot.', 'Burnout prevention tips for overworked robots.', 'Designing a CLI tool for cavemen.', 'Technical interview questions for mythical creatures.', 'Incident playbook for mind-reading AI misfires.', 'Retrospective notes from a failed Mars deployment.', 'Slackbot that refuses to answer HR questions.', 'Onboarding guide for interdimensional interns.', 'Terraform script for castle infrastructure.', 'Compliance checklist for AI whisperers.', 'CI/CD pipeline for enchanted artifacts.', 'Project plan written entirely in limericks.', 'DNS issues caused by quantum entanglement.', 'Command line tool for managing alternate timelines.', 'A11y plan for ghosts in augmented reality apps.', "Traceback from a dream interpreter's API."]

class EmbedRequest(BaseModel):
    content: str

class QueryRequest(BaseModel):
    prompt: str

@app.get("/status")
async def status():
    return {
        "ollama_model": "mistral",
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
    return {
        "message": "Files uploaded and embedded",
        "documents_indexed": accepted,
        "documents_skipped": skipped
    }

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