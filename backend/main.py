from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Literal
import os
import shutil

from pdf_ingest import extract_pdf_text
from youtube_ingest import fetch_transcript
from chunker import chunk_text
from embedder import embed_chunks
from vector_store import VectorStore
from chat_service import chat

# --------------------------------------------------
# APP SETUP
# --------------------------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# GLOBAL KNOWLEDGE BASE
# --------------------------------------------------

vector_store = None          # initialized on first ingest
all_chunks: list = []        # stores ALL chunks (PDF + YouTube)

UPLOAD_DIR = "data/uploads"

# --------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "ok"}

# --------------------------------------------------
# REQUEST MODELS
# --------------------------------------------------

class HistoryItem(BaseModel):
    role: Literal["student", "teacher"]
    content: str

class ChatRequest(BaseModel):
    question: str
    history: List[HistoryItem] = []
    difficulty: str = "normal"

# --------------------------------------------------
# INGEST DEFAULT PDF ON STARTUP (OPTIONAL)
# --------------------------------------------------

@app.on_event("startup")
def ingest_default_pdf():
    global vector_store

    try:
        pages = extract_pdf_text("")
        chunks = chunk_text(pages)
        embedded = embed_chunks(chunks)

        # Initialize vector store safely
        if vector_store is None:
            vector_store = VectorStore(
                dimension=len(embedded[0]["embedding"])
            )

        vector_store.add(embedded)
        all_chunks.extend(chunks)

        print("✅ Default PDF ingested")

    except Exception as e:
        print("⚠️ Default PDF not loaded:", e)

# --------------------------------------------------
# CHAT ENDPOINT
# --------------------------------------------------

@app.post("/chat")
def chat_endpoint(payload: ChatRequest):
    if not all_chunks:
        return {
            "teacher": "No documents have been uploaded yet.",
            "student": "",
            "teacher_followup": "",
            "sources": []
        }

    return chat(
        question=payload.question,
        history=payload.history,
        vector_store=vector_store,
        chunks=all_chunks
    )

# --------------------------------------------------
# PDF INGEST ENDPOINT
# --------------------------------------------------

@app.post("/ingest/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    global vector_store

    # ✅ Ensure upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    pdf_path = os.path.join(UPLOAD_DIR, file.filename)

    # ✅ Save file safely
    with open(pdf_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    pages = extract_pdf_text(pdf_path)
    chunks = chunk_text(pages)
    embedded = embed_chunks(chunks)

    # ✅ Initialize vector store if needed
    if vector_store is None:
        vector_store = VectorStore(
            dimension=len(embedded[0]["embedding"])
        )

    vector_store.add(embedded)
    all_chunks.extend(chunks)

    return {
        "status": "success",
        "pdf": file.filename,
        "chunks_added": len(chunks)
    }

# --------------------------------------------------
# YOUTUBE INGEST ENDPOINT
# --------------------------------------------------

@app.post("/ingest/youtube")
def ingest_youtube(url: str):
    global vector_store

    try:
        pages = fetch_transcript(url)
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

    chunks = chunk_text(pages)
    embedded = embed_chunks(chunks)

    if vector_store is None:
        vector_store = VectorStore(
            dimension=len(embedded[0]["embedding"])
        )

    vector_store.add(embedded)
    all_chunks.extend(chunks)

    return {
        "status": "success",
        "chunks_added": len(chunks)
    }
