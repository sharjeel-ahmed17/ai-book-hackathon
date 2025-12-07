---
id: 1
title: Update RAG Chatbot Constitution
stage: constitution
date: 2025-12-07
surface: agent
model: qwen
feature: none
branch: backend
user: SHARJEELAHMED
command: sp.constitution
labels: [constitution,rag,chatbot]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

```
Project: Integrated RAG Chatbot for a Published Book

Core principles:
- Answers strictly grounded in book content
- Retrieval-first, zero-hallucination behavior
- Transparent and traceable responses
- Clear, maintainable system design

Key standards:
- Responses generated only from retrieved text
- Source references included in answers
- Support full-book and user-selected-text Q&A
- Stack: OpenAI Agents/ChatKit, FastAPI, Qdrant, Neon Postgres , co here

Constraints:
- No external knowledge usage
- Free-tier friendly infrastructure
- Low-latency, in-book interaction

Quality & validation:
- Hallucination tolerance: 0%
- Retrieval relevance validated
- Fallback on low confidence

Success criteria:
- Accurate, source-grounded answers
- Stable backend and book integration
```

## Response snapshot

Updated the constitution file to reflect the Integrated RAG Chatbot for a Published Book project, replacing the previous Physical AI Humanoid Robotics Textbook content. The new constitution includes core principles focused on content grounding, retrieval-first architecture, transparency, AI-assisted development, full-book and selective Q&A support, and stack-driven implementation. The version was updated from 1.0.0 to 1.1.0 with updated dates.

## Outcome

- ✅ Impact: Constitution updated to reflect RAG Chatbot project requirements
- 🧪 Tests: N/A
- 📁 Files: Updated .specify/memory/constitution.md with new project focus
- 🔁 Next prompts: Plan and implement RAG chatbot features
- 🧠 Reflection: Successfully transitioned project constitution from robotics textbook to RAG chatbot

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin feature specification for RAG chatbot