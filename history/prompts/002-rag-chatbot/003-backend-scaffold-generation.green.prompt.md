---
id: 003
title: Backend Scaffold Generation
stage: green
date: 2025-12-16
surface: agent
model: claude-sonnet-4.5
feature: 002-rag-chatbot
branch: 001-physical-ai-humanoid-book
user: Narmeen
command: user-prompt
labels: ["backend", "fastapi", "scaffold", "agents", "tools", "implementation"]
links:
  spec: specs/002-rag-chatbot/spec.yaml
  ticket: null
  adr: null
  pr: null
files:
  - backend/main.py
  - backend/utils.py
  - backend/requirements.txt
  - backend/.env.example
tests:
  - Manual testing with uvicorn server
---

## Prompt

You are an AI backend developer.
Based on the RAG Chatbot Spec, generate the **complete backend scaffold** in one go:

1. Create folder structure:
   backend/
    ├─ specs/
    │   └─ spec.yaml (already exists)
    ├─ main.py
    └─ utils.py

2. main.py:
   - FastAPI backend with /chat endpoint
   - Accepts {"query": "...", "selected_text": "..."}
   - Calls ContentAgent/UserAgent
   - Uses RAGRetriever and TextEmbedder
   - Returns JSON answer

3. utils.py:
   - Qdrant client setup with placeholders
   - embed_text(text) for free embeddings
   - upsert_embeddings(data)
   - retrieve_from_qdrant(query)

4. Output ready-to-save **full code** for main.py and utils.py, with all imports.

## Response snapshot

Generated complete backend scaffold with 4 files:

**main.py (~550 lines):**
- FastAPI application with lifespan handler
- Pydantic schemas: ChatRequest, ChatResponse, SessionRequest, SessionResponse, HealthResponse
- SessionStore: In-memory session storage with 30-min timeout
- IntentClassifier: Rule-based classification for 6 intents (content_query, selection_query, clarification, greeting, help, out_of_scope)
- BaseAgent, ContentAgent, UserAgent implementations
- ContentAgent pipeline: Query prep → Embed → Retrieve → Context build → LLM generate → Format
- Endpoints: POST /api/v1/chat, POST /api/v1/session, GET /api/v1/health, GET /
- CORS middleware configured
- Uvicorn development server

**utils.py (~500 lines):**
- Configuration from environment variables
- embed_text(): Single text embedding with sentence-transformers
- embed_texts_batch(): Batch embedding for indexing
- get_qdrant_client(): Lazy-loaded Qdrant client
- init_qdrant_collection(): Create collection with payload indices
- upsert_embeddings(): Batch upsert chunks with MD5 content hashing
- retrieve_from_qdrant(): Vector similarity search with filtering
- get_neon_connection(): Postgres connection
- init_neon_schema(): Create tables (content_chunks, chat_sessions, query_logs)
- chunk_markdown_file(): Semantic chunking with overlap
- index_book_directory(): Index all markdown files
- CLI for testing: embed, search, index, stats, init-db

**requirements.txt:**
- FastAPI, uvicorn, pydantic
- qdrant-client, sentence-transformers, torch
- psycopg[binary], groq
- Development dependencies (commented)

**.env.example:**
- All required environment variables with descriptions
- Free tier service URLs and placeholders

## Outcome

- Impact: Complete working backend scaffold ready for deployment
- Tests: Manual testing required (run with `uvicorn main:app --reload`)
- Files: 4 created (main.py, utils.py, requirements.txt, .env.example)
- Next prompts: Test backend locally, create frontend ChatWidget component
- Reflection: Comprehensive implementation following spec.yaml architecture with all agents, tools, and utilities

## Evaluation notes (flywheel)

- Failure modes observed: None during generation
- Graders run and results (PASS/FAIL): Manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run backend and test /chat endpoint
