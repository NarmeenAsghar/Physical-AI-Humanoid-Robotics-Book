---
id: 002
title: RAG Chatbot Architectural Plan Creation
stage: plan
date: 2025-12-16
surface: agent
model: claude-sonnet-4.5
feature: 002-rag-chatbot
branch: 001-physical-ai-humanoid-book
user: Narmeen
command: user-prompt
labels: ["architecture", "plan", "rag", "fastapi", "agents", "data-flow"]
links:
  spec: specs/002-rag-chatbot/spec.yaml
  ticket: null
  adr: null
  pr: null
files:
  - specs/002-rag-chatbot/plan.yaml
tests:
  - N/A (architectural plan document)
---

## Prompt

You are an AI system architect.
Based on the generated RAG Chatbot Spec (`specs/002-rag-chatbot/spec.yaml`), create a detailed **architectural plan** for implementation.

Requirements:
- Include all components: FastAPI backend, Neon Postgres, Qdrant, LLM, embeddings.
- Include data flow from user query → selection → retrieval → response.
- Include agents (ContentAgent, UserAgent) and tools (RAGRetriever, TextEmbedder) interactions.
- Specify folder/file layout for implementation.
- Output plan in Spec-Kit Plus /sp.plan compatible YAML.

## Response snapshot

Created comprehensive architectural plan (`specs/002-rag-chatbot/plan.yaml`) with:

**System Architecture (11 Components):**
- Frontend: Docusaurus Chat Widget (React)
- API Gateway: FastAPI Backend
- Agent Layer: UserAgent, ContentAgent, Orchestrator
- Tool Layer: TextEmbedder, RAGRetriever
- Services: LLMClient, SessionManager, IntentClassifier
- Data Layer: NeonClient, QdrantClient

**Data Flow Diagrams (3 Flows):**
1. Query Flow: 14-step flow from user question to response
2. Selection Flow: 6-step text selection context capture
3. Indexing Flow: 5-step batch book content indexing

**Agent Interactions:**
- UserAgent: Rule-based intent classification (6 intents), routing logic
- ContentAgent: 5-stage pipeline (Query Prep → Retrieval → Context → Generation → Formatting)

**Project Structure:**
- `backend/` - FastAPI app with agents/, tools/, services/, db/, api/
- `website/src/` - ChatWidget component, hooks, services
- `scripts/` - Dev, deploy, index scripts

**Key Design Decisions (6 ADR candidates):**
- DD-001: Multi-Agent Architecture
- DD-002: In-Memory Session Storage
- DD-003: Local Embedding Generation
- DD-004: Qdrant Cloud over ChromaDB
- DD-005: Groq for LLM
- DD-006: Rule-Based Intent Classification

**4 Implementation Phases defined with deliverables and success criteria**

## Outcome

- Impact: Complete architectural blueprint for RAG chatbot implementation
- Tests: N/A (architectural plan, not implementation)
- Files: 1 created (specs/002-rag-chatbot/plan.yaml)
- Next prompts: /sp.tasks to generate detailed implementation tasks
- Reflection: Comprehensive plan covering all requested components with clear data flows, agent interactions, and file structure

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Validate plan completeness against spec requirements
