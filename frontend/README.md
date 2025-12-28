# 📘 Interactive Study Tool (NotebookLM-Inspired)

An **AI-powered study assistant** that allows students to upload **PDFs and YouTube videos**, build a **knowledge base**, and ask questions that are answered **strictly from the provided sources**.

This system is **source-grounded**, **hallucination-free**, and designed for **deep learning, revision, and exam preparation**.

---

## 🚀 Features

### 📄 Multi-Source Knowledge Ingestion
- Upload **multiple PDFs**
- Ingest **YouTube videos** using transcripts
- Combine PDFs + videos into a single knowledge base

### 🧠 Retrieval-Augmented Generation (RAG)
- Content is chunked and embedded
- Stored in **FAISS vector database**
- Semantic retrieval ensures **only relevant context** is used
- AI answers **ONLY from ingested sources**

### 👩‍🏫 Teacher-Style AI Responses
- Step-by-step explanations
- Simple, student-friendly language
- Student follow-up questions + clarifications
- Source references included

### 💬 Conversational Memory
- Maintains chat history
- Context-aware follow-up questions
- Student ↔ Teacher dialogue format

---

## 🧱 Tech Stack

### Frontend
- **Next.js (App Router)**
- React + TypeScript
- Fetch API

### Backend
- **FastAPI (Python)**
- FAISS (Vector Search)
- Gemini AI (LLM)
- PyMuPDF (PDF parsing)
- youtube-transcript-api (YouTube ingestion)

---

## 🗂 Project Structure

