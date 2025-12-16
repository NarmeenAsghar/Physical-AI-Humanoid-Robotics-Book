---
id: 004
title: Frontend Chatbot Component Generation
stage: green
date: 2025-12-16
surface: agent
model: claude-sonnet-4.5
feature: 002-rag-chatbot
branch: 001-physical-ai-humanoid-book
user: Narmeen
command: user-prompt
labels: ["frontend", "react", "docusaurus", "chatbot", "component", "css"]
links:
  spec: specs/002-rag-chatbot/spec.yaml
  ticket: null
  adr: null
  pr: null
files:
  - website/src/components/Chatbot/Chatbot.js
  - website/src/components/Chatbot/Chatbot.module.css
  - website/src/components/Chatbot/index.js
  - website/src/theme/Root.js
tests:
  - Manual testing in Docusaurus dev server
---

## Prompt

You are an AI frontend developer.
Generate a React component for Docusaurus book to query the RAG chatbot:

Requirements:
- Input box for user query
- Button to submit query
- Calls FastAPI /chat endpoint
- Displays answer
- Optional: highlight selected text from page and send to backend
- Simple styling compatible with light/dark mode
- Output code ready to save as `docusaurus/src/components/Chatbot.js`

## Response snapshot

Generated complete React chatbot widget with 4 files:

**Chatbot.js (~400 lines):**
- Custom hooks:
  - `useTextSelection()`: Captures text selected on page (excludes chatbot widget)
  - `useChatSession()`: Manages session ID creation/retrieval
- Sub-components:
  - `MessageBubble`: Renders user/bot messages with sources and confidence
  - `SelectionContext`: Shows selected text context indicator
  - `LoadingIndicator`: Animated loading dots
  - `ChatInput`: Form with input and send button
- Main `Chatbot` component:
  - Floating toggle button
  - Chat window with header, messages area, input
  - Welcome message on first open
  - API integration with error handling
  - Auto-scroll to latest message

**Chatbot.module.css (~450 lines):**
- CSS custom properties for theming
- Light/dark mode support via `[data-theme='dark']`
- Responsive design (mobile breakpoint at 480px)
- Smooth animations (slide-up, typing indicator)
- Accessibility support (reduced motion, focus-visible)
- Scrollbar styling
- Source citation tags
- Selection context styling

**index.js:**
- Clean export for import convenience

**Root.js:**
- Docusaurus theme wrapper to inject chatbot on all pages

## Outcome

- Impact: Complete frontend chatbot widget ready for Docusaurus integration
- Tests: Manual testing required (run Docusaurus dev server)
- Files: 4 created (Chatbot.js, Chatbot.module.css, index.js, Root.js)
- Next prompts: Configure API URL environment variable, test end-to-end
- Reflection: Full-featured component with text selection, dark mode, and responsive design

## Evaluation notes (flywheel)

- Failure modes observed: None during generation
- Graders run and results (PASS/FAIL): Manual testing required
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test chatbot with running backend
