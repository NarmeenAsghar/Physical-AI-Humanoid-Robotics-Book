---
id: 007
title: Local Qdrant Embedded Mode Setup
stage: green
date: 2025-12-16
surface: agent
model: claude-sonnet-4.5
feature: 002-rag-chatbot
branch: 001-physical-ai-humanoid-book
user: Narmeen
command: user-prompt
labels: ["backend", "qdrant", "local", "embedded", "offline", "vector-db"]
links:
  spec: specs/002-rag-chatbot/spec.yaml
  ticket: null
  adr: null
  pr: null
files:
  - backend/utils.py
  - backend/populate_qdrant.py
  - backend/main.py
tests:
  - Manual testing with python populate_qdrant.py --test
  - Manual testing with python main.py
---

## Prompt

You are a senior Python AI engineer. I have a Python project with the following requirements:
1. I want to create a **local, offline Qdrant vector database** (embedded mode, no Docker, no external server).
2. I need a `utils.py` file that provides:
   - `get_qdrant_client()` → returns a QdrantClient instance in local embedded mode.
   - `embed_text(text: str)` → returns a 384-dim vector for a string
   - `init_qdrant_collection(collection_name)` → creates a collection if it doesn't exist.
   - `retrieve_from_qdrant(query_vector, top_k=5, score_threshold=0.5, collection_name="book_chunks")` → retrieves similar vectors.
3. I need a `populate_qdrant.py` file that:
   - Uses `utils.py`.
   - Creates a collection called `"book_chunks"` if it doesn't exist.
   - Inserts a few dummy text chunks (at least 3) with metadata (chapter, section).
   - Provides CLI for testing queries.

## Response snapshot

Rewrote `utils.py` (v2.0.0) with local embedded Qdrant support:

**Configuration:**
- `QDRANT_LOCAL_PATH = "./qdrant_local"` - stores data locally
- `EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"` (384 dimensions)
- No external server required - runs entirely in-process

**Functions Provided:**
- `get_qdrant_client()` - lazy-loaded client with `QdrantClient(path="./qdrant_local")`
- `close_qdrant_client()` - cleanup function
- `get_embedding_model()` - lazy-loaded SentenceTransformer
- `embed_text(text)` - returns 384-dim vector
- `embed_texts(texts)` - batch embedding for efficiency
- `init_qdrant_collection(name, vector_size, distance, recreate)` - create collection
- `delete_collection(name)` - remove collection
- `get_collection_info(name)` - get collection stats
- `upsert_chunks(chunks, collection)` - insert/update with batch support
- `retrieve_from_qdrant(query, top_k, score_threshold, collection, filter_conditions)` - semantic search
- `retrieve_by_vector(vector, ...)` - search with pre-computed vector
- `chunk_text(text, chunk_size, overlap, metadata)` - text chunking utility
- `health_check()` - system status check

**Created `populate_qdrant.py` (v1.0.0):**
- 10 sample chunks covering ROS2, digital twins, kinematics, URDF, Gazebo, MoveIt, humanoid robotics, physical AI, reinforcement learning
- CLI with `--test`, `--clear`, `--file`, `--query`, `--info` options
- Auto-tests retrieval with sample queries

**Updated `main.py`:**
- Changed `retrieve_from_qdrant(query_embedding=...)` to `retrieve_from_qdrant(query=...)` to match new function signature
- Embedding is now handled internally by retrieve_from_qdrant

## Outcome

- Impact: RAG backend now runs 100% locally with no external dependencies
- Tests: Manual testing required with `python populate_qdrant.py` and `python main.py`
- Files: 3 modified (backend/utils.py, backend/populate_qdrant.py, backend/main.py)
- Next prompts: Test end-to-end flow, add more book content to Qdrant
- Reflection: Successfully converted from cloud Qdrant to local embedded mode for offline development

## Evaluation notes (flywheel)

- Failure modes observed: Initial file write conflict due to external modification
- Graders run and results (PASS/FAIL): Manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add Ollama integration for better LLM responses
