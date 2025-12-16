---
id: 001
title: RAG Chatbot Specification Generation
stage: spec
date: 2025-12-16
surface: agent
model: claude-sonnet-4.5
feature: 002-rag-chatbot
branch: 001-physical-ai-humanoid-book
user: Narmeen
command: user-prompt
labels: ["rag", "chatbot", "specification", "yaml", "fastapi", "qdrant", "neon"]
links:
  spec: specs/002-rag-chatbot/spec.yaml
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-rag-chatbot/spec.yaml
tests:
  - N/A (specification document)
---

## Prompt

You are an AI engineer. Generate a Spec-Kit Plus specification file for a Retrieval-Augmented Generation (RAG) chatbot that will be embedded in a Docusaurus book.
Constraints:
- The chatbot should answer questions only from the book's content.
- It should allow users to select text in the book and answer based on that selection.
- Must be fully free: use Neon Serverless Postgres and Qdrant Free Tier.
- Use FastAPI as backend.
- Define at least 2 agents: "ContentAgent" (handles book content queries) and "UserAgent" (handles user interactions).
- Define tools: "RAGRetriever" (fetches relevant book paragraphs) and "TextEmbedder" (converts text to embeddings for Qdrant).
- Include proper spec structure compatible with Spec-Kit Plus.
- Output the spec in YAML format.

## Response snapshot

Generated a comprehensive Spec-Kit Plus compatible YAML specification file for the RAG chatbot with:

**Infrastructure:**
- FastAPI backend with Python 3.11+
- Neon Serverless Postgres (Free tier: 512MB, 191.9 compute hours/month)
- Qdrant Cloud (Free tier: 1M vectors)
- Groq LLM API (Free tier: 30 req/min)
- HuggingFace sentence-transformers (all-MiniLM-L6-v2, 384 dimensions)

**Agents:**
1. **ContentAgent**: Handles book content queries, orchestrates retrieval, synthesizes answers with citations
2. **UserAgent**: Manages user interactions, intent classification, session management, routing

**Tools:**
1. **RAGRetriever**: Fetches relevant chunks via Qdrant similarity search with filtering
2. **TextEmbedder**: Generates 384-dim embeddings using sentence-transformers

**Data Model:**
- Neon tables: content_chunks, chat_sessions, query_logs
- Qdrant collection: book_chunks with HNSW indexing

**User Stories (P1-P2):**
- US-001: Ask questions about book content
- US-002: Explain selected text
- US-003: Follow-up questions
- US-004: Fast response times (<3s p95)

## Outcome

- Impact: Created foundational specification for RAG chatbot feature
- Tests: N/A (specification document, not implementation)
- Files: 1 created (specs/002-rag-chatbot/spec.yaml)
- Next prompts: /sp.plan to create architectural plan, /sp.tasks to generate implementation tasks
- Reflection: Comprehensive spec covering all requested constraints with free-tier infrastructure, two agents, two tools, and Spec-Kit Plus compatible structure

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate YAML structure against Spec-Kit Plus parser
