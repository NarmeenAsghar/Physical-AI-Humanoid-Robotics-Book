---
id: 006
title: Frontend Chatbot Docusaurus-Safe Rewrite
stage: green
date: 2025-12-16
surface: agent
model: claude-sonnet-4.5
feature: 002-rag-chatbot
branch: 001-physical-ai-humanoid-book
user: Narmeen
command: user-prompt
labels: ["frontend", "react", "docusaurus", "security", "no-secrets", "refactor"]
links:
  spec: specs/002-rag-chatbot/spec.yaml
  ticket: null
  adr: null
  pr: null
files:
  - website/src/components/Chatbot/Chatbot.js
tests:
  - Manual testing in Docusaurus dev server
---

## Prompt

You are an AI frontend developer working with Docusaurus and a FastAPI backend.

Task: Rewrite `Chatbot.js` to be **Docusaurus-compatible** and **backend-safe**. Follow these rules:

1. **No direct use of Node.js `process`** in the frontend.
   - All secret keys (Qdrant, Neon, LLM) must be accessed only via backend endpoints.
   - Frontend must **never include API keys**.

2. **Frontend functionality**:
   - User can type a query and optionally select some text from the book.
   - Send the query + selected text to backend endpoint `/chat` (POST JSON: `{query, selected_text}`).
   - Display the response from backend (answer + sources) in a chat UI.

3. **React / Docusaurus compatible**:
   - Use functional components and hooks (`useState`, `useEffect`).
   - Include simple chat UI: messages list, input box, send button.
   - Clear previous messages if needed.
   - Style minimally (inline CSS or simple classNames).

4. **Handle errors**:
   - Show a friendly message if backend request fails.
   - Disable input while waiting for response.

5. **Output**:
   - Full ready-to-use `Chatbot.js` content
   - Docusaurus `src/components/Chatbot/Chatbot.js` compatible
   - Include docstrings / comments explaining important parts

Important: All backend calls must go to `https://narmeenasghar-rag-chatbot.hf.space/chat` or relative path. Do **not include any secret keys** in the frontend code.

## Response snapshot

Rewrote `Chatbot.js` (v2.0.0) with the following security and compatibility improvements:

**Security Changes:**
- Removed `process.env.REACT_APP_API_URL` - No process.env in browser
- Hardcoded `BACKEND_URL = 'https://narmeenasghar-rag-chatbot.hf.space'` with clear comments
- Uses simplified `/chat` endpoint instead of `/api/v1/chat`
- NO API keys, secrets, or Authorization headers in frontend
- All sensitive operations (Qdrant, embeddings) handled by backend

**Removed:**
- `useChatSession()` hook (session management simplified)
- Complex API_ENDPOINTS object
- References to process.env

**Simplified:**
- Direct fetch to `CHAT_ENDPOINT = BACKEND_URL + '/chat'`
- Request body: `{ query, selected_text }` only
- Response parsing: `{ answer, sources, confidence }`
- Error messages include troubleshooting steps

**Added:**
- Comprehensive JSDoc comments throughout
- Security notes in docstrings
- `typeof window !== 'undefined'` checks for SSR safety
- Explicit `type="button"` on all buttons
- `autoComplete="off"` on input

**Structure:**
- `useTextSelection()` - Captures page text selection
- `MessageBubble` - Renders message with sources
- `SelectionContext` - Shows selected text indicator
- `TypingIndicator` - Animated loading dots
- `ChatInput` - Form with input and submit
- `Chatbot` - Main component with all state

## Outcome

- Impact: Frontend now safe for Docusaurus with no secret exposure
- Tests: Manual testing required
- Files: 1 modified (website/src/components/Chatbot/Chatbot.js)
- Next prompts: Test end-to-end with backend running
- Reflection: Comprehensive rewrite with security-first approach and extensive documentation

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add environment-based URL switching for production
