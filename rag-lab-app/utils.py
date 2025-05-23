
import os
import json
import fitz  # PyMuPDF
import docx
import hashlib

from typing import List


def extract_text(file_path: str) -> str:
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".txt":
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    elif ext == ".pdf":
        text = ""
        with fitz.open(file_path) as pdf:
            for page in pdf:
                text += page.get_text()
        return text
    elif ext == ".docx":
        doc = docx.Document(file_path)
        return "".join([para.text for para in doc.paragraphs])
    else:
        raise ValueError(f"Unsupported file type: {ext}")


def embed_text(text: str) -> List[str]:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return lines


def load_documents(file_path: str = "documents.json") -> List[str]:
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_documents(docs: List[str], file_path: str = "documents.json"):
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)


def file_hash(path: str) -> str:
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        hasher.update(f.read())
    return hasher.hexdigest()
