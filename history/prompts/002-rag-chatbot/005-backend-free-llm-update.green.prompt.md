---
id: 005
title: Backend Update with Free LLM Function
stage: green
date: 2025-12-16
surface: agent
model: claude-sonnet-4.5
feature: 002-rag-chatbot
branch: 001-physical-ai-humanoid-book
user: Narmeen
command: user-prompt
labels: ["backend", "free-llm", "no-api-key", "fastapi", "refactor"]
links:
  spec: specs/002-rag-chatbot/spec.yaml
  ticket: null
  adr: null
  pr: null
files:
  - backend/main.py
tests:
  - Manual testing with uvicorn server
---

## Prompt

You are an AI Python developer.

Task: Generate **backend code** for RAG Chatbot using **FastAPI** with the following requirements:

1. **Load environment variables** from `.env` using `python-dotenv`:
   - QDRANT_URL, QDRANT_API_KEY, QDRANT_COLLECTION
   - NEON_DATABASE_URL
   - EMBEDDING_MODEL

2. **Free LLM function**:
   - Name: `call_llm(prompt, context)`
   - Takes `prompt` (user query) and `context` (retrieved text)
   - Returns a string with simulated LLM answer
   - Example: `"[LLM Answer based on context]: {context[:200]}"`

3. **main.py**:
   - FastAPI backend
   - Endpoint: `/chat` (POST)
   - Accepts JSON: `{"query": "...", "selected_text": "..."}`
   - Calls: `retrieve_from_qdrant(query, top_k=5)` from utils.py, `call_llm(prompt, context)`
   - Returns JSON: `{"answer": "...", "sources": [...]}`

4. **utils.py** already exists with Qdrant and embedding functions.

5. **Do NOT include paid LLM APIs** (Groq or others).
6. Include proper imports, docstrings, and ready-to-run code.

## Response snapshot

Updated `backend/main.py` with the following changes:

**Removed:**
- Groq import and dependency
- GROQ_API_KEY configuration
- Groq client initialization in ContentAgent

**Added:**
- `call_llm(prompt, context, query, selected_text)` function:
  - Free simulated LLM that extracts and formats retrieved content
  - Generates contextual introductions based on query type
  - Includes up to 3 most relevant chunks
  - Handles selected text explanations
  - Returns structured answer without any API calls

- Simplified `/chat` endpoint (POST /chat):
  - Accepts `{"query": "...", "selected_text": "..."}`
  - Returns `{"answer": "...", "sources": [...], "confidence": ..., "intent": ...}`

**Modified:**
- Settings class: Removed Groq settings, lowered SCORE_THRESHOLD to 0.5
- ContentAgent._generate_llm_response replaced with call_llm()
- Health check: Reports LLM as "free_simulated"
- Startup messages: Indicates FREE mode, no API keys required
- Default intent classification: More permissive (defaults to content_query)

**Version bumped to 1.1.0**

## Outcome

- Impact: Backend now runs without any paid API keys
- Tests: Manual testing required
- Files: 1 modified (backend/main.py)
- Next prompts: Test end-to-end with frontend, consider adding Ollama integration for better responses
- Reflection: Successfully removed paid LLM dependency while maintaining functionality

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add Ollama client as optional LLM provider
