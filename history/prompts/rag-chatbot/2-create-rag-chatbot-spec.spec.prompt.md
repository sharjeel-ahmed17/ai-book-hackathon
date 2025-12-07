---
id: 2
title: Create RAG Chatbot Spec
stage: spec
date: 2025-12-07
surface: agent
model: qwen
feature: rag-chatbot
branch: 001-rag-chatbot
user: SHARJEELAHMED
command: sp.specify
labels: [spec,rag,chatbot,book]
links:
  spec: specs/001-rag-chatbot/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-rag-chatbot/spec.md
 - specs/001-rag-chatbot/checklists/requirements.md
 - .specify/memory/constitution.md
tests:
 - null
---

## Prompt

```
/sp.specify Integrated RAG Chatbot for Published Book

Target audience:
- Technical readers of the book (students, developers, researchers)
- Engineers evaluating in-book AI assistants

Focus:
- Build a RAG chatbot embedded in the published book
- Answers grounded in full-book or selected-text content only
- Project structure inside `chatbot/` directory

Success criteria:
- Chatbot responses fully grounded in book content
- Correct handling of selected-text queries
- Zero hallucination
- Clear, reproducible architecture documented

Constraints:
- Stack: OpenAI Agents / ChatKit SDKs, FastAPI, Qdrant Cloud Free Tier, Neon Serverless Postgres
- Markdown source format
- Free-tier compatible
- Low-latency (<2s) responses

Not building:
- General-purpose chatbot unrelated to book
- LLM fine-tuning
- Full-scale UI beyond embedding

Chapters / Steps:

1. RAG (Retrieval-Augmented Generation)
   - Define problem: answer user queries over book content
   - Design retrieval-first prompt structure
   - Implement query handling for full-book and selected-text contexts
   - Reference: OpenAI Agents / ChatKit

2. Embedding
   - Chunk book content and metadata
   - Generate embeddings for retrieval
   - Store embedding pipeline in `chatbot/embedding/`
   - Tools: OpenAI embeddings or equivalent

3. Convert
   - Convert book content into structured, retrievable format
   - Prepare documents for ingestion into vector database
   - Include support for text selection by user
   - Store conversion scripts in `chatbot/convert/`

4. Vector Database
   - Set up Qdrant Cloud Free Tier as vector store
   - Integrate Neon Serverless Postgres for session and metadata
   - Implement retrieval API with FastAPI in `chatbot/api/`
   - Validate retrieval accuracy and grounding

Reference links:
- https://ai-book-hackathon-two.vercel.app/
- Qdrant Cloud client: `QdrantClient(url=..., api_key=...)`
- Neon Postgres: `DATABASE_URL=postgresql://neondb_owner:...`
- Cohere API: `cohere_api_key=TBzr37EHlK7ZNCxtH8XcApXOJPyYbvB10IPGT6o8`
```

## Response snapshot

Created the specification for the Integrated RAG Chatbot for Published Book feature. The specification includes:
- User scenarios for querying book content with full-book context (P1), selected text sections (P2), and source attribution (P3)
- Functional requirements focusing on content grounding, source references, query handling, and performance
- Success criteria measuring hallucination prevention, response times, source attribution, and query accuracy
- Alignment with the RAG Chatbot constitution principles
- Quality checklist validating all requirements

The spec is technology-agnostic where appropriate and focuses on user value rather than implementation details.

## Outcome

- ✅ Impact: Complete specification created for RAG chatbot feature
- 🧪 Tests: N/A
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: Successfully translated technical requirements into user-focused specification

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin planning the RAG chatbot implementation