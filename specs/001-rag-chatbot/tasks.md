# Tasks: Integrated RAG Chatbot for Published Book

**Feature**: Integrated RAG Chatbot for Published Book | **Branch**: 001-rag-chatbot
**Input**: Design documents from `/specs/001-rag-chatbot/`

## Implementation Strategy

This implementation follows a phased approach with user stories prioritized as P1, P2, P3. Each phase delivers independently testable functionality aligned with the feature specification. The MVP scope includes User Story 1 (full-book querying) with source attribution, which forms the core RAG functionality.

## Dependencies

- User Story 2 (selected-text queries) depends on foundational components from User Story 1
- User Story 3 (source attribution) is integrated into both previous stories
- All stories depend on setup and foundational phases

## Parallel Execution Examples

- Model creation tasks can run in parallel (T005, T006, T007, T008)
- Service implementations can run in parallel after models are defined
- API endpoint creation can run in parallel after service implementations

---

## Phase 1: Setup

Initialize project structure and configure dependencies for the RAG chatbot.

- [X] T001 Create project directory structure under chatbot/
- [X] T002 Initialize Python project with requirements.txt containing FastAPI, Qdrant, Cohere, psycopg2-binary, python-dotenv, openai, google-generativeai
- [X] T003 Create configuration module with settings for Qdrant, Cohere, Neon Postgres, and Google Gemini API keys
- [X] T004 Set up environment variables for all API keys and database connections

---

## Phase 2: Foundational Components

Implement core infrastructure components needed by all user stories.

- [X] T005 [P] Create Query model in chatbot/core/models/query.py with fields for query_id, session_id, content, context_type, selected_text, timestamp, source_references
- [X] T006 [P] Create RetrievedContext model in chatbot/core/models/retrieved_context.py with fields for context_id, query_id, content_chunks, metadata
- [X] T007 [P] Create Response model in chatbot/core/models/response.py with fields for response_id, query_id, content, source_references, timestamp, validation_status
- [X] T008 [P] Create ConversationSession model in chatbot/core/models/conversation_session.py with fields for session_id, user_id, created_at, last_activity, queries, metadata
- [X] T009 [P] Create BookContent model in chatbot/core/models/book_content.py with fields for content_id, book_id, title, content_text, metadata, embedding_vector, source_reference
- [X] T010 [P] Create UserSessionPreference model in chatbot/core/models/user_session_preference.py with fields for preference_id, session_id, query_context_default, response_format, source_citation_preference, created_at, updated_at
- [X] T011 [P] Create Qdrant storage integration in chatbot/core/storage/vector_db.py
- [X] T012 [P] Create Neon Postgres storage integration in chatbot/core/storage/metadata_db.py
- [X] T013 [P] Create embedding processor in chatbot/core/embeddings/processor.py
- [X] T014 [P] Create content converter utilities in chatbot/services/content_converter.py
- [X] T015 [P] Create text chunker utilities in chatbot/services/chunker.py
- [X] T016 [P] Create session manager in chatbot/services/session_manager.py
- [X] T017 [P] Create input/output validators in chatbot/utils/validators.py
- [X] T018 [P] Create RAG retriever logic in chatbot/core/rag/retriever.py
- [X] T019 [P] Create RAG generator logic in chatbot/core/rag/generator.py
- [X] T020 [P] Create RAG validator for content grounding in chatbot/core/rag/validator.py
- [X] T021 Create health check endpoint in chatbot/api/routers/health.py
- [X] T022 Create API request/response models in chatbot/api/models/request.py
- [X] T023 Create API request/response models in chatbot/api/models/response.py

---

## Phase 3: User Story 1 - Query Book Content with Full-Book Context (Priority: P1)

As a technical reader of the book, I want to ask questions about the book content and receive answers that are strictly grounded in the book's content so that I can get accurate information without any hallucinated responses.

**Independent Test**: Can be fully tested by submitting queries to the chatbot and verifying that responses are based only on book content with proper source attribution, delivering the fundamental value of the RAG system.

- [X] T024 [P] [US1] Create query endpoint in chatbot/api/routers/query.py
- [X] T025 [US1] Create query service in chatbot/services/query_service.py that handles full-book context queries
- [X] T026 [US1] Implement RAG pipeline for full-book queries in chatbot/core/rag/pipeline.py
- [X] T027 [US1] Integrate embedding generation for book content with Cohere/Gemini in chatbot/core/embeddings/content_embedder.py
- [X] T028 [US1] Implement content retrieval from Qdrant for full-book context via RAGRetriever in chatbot/core/rag/retriever.py
- [X] T029 [US1] Implement response generation with proper source attribution via RAGGenerator in chatbot/core/rag/generator.py
- [X] T030 [US1] Add hallucination validation to ensure content grounding via RAGValidator in chatbot/core/rag/validator.py
- [X] T031 [US1] Test full-book query functionality with sample book content in test_sample_query.py

---

## Phase 4: User Story 2 - Query Selected Text Sections (Priority: P2)

As a technical reader, I want to select specific text sections from the book and ask questions about only those sections so that I can get focused answers relevant to my specific area of interest.

**Independent Test**: Can be tested by allowing users to select text portions and then asking questions, verifying that responses are limited to the selected text context.

- [X] T032 [P] [US2] Create ingestion endpoint in chatbot/api/routers/ingest.py
- [X] T033 [US2] Implement selected-text query handling in chatbot/services/query_service.py
- [X] T034 [US2] Extend RAG pipeline to support selected-text context in chatbot/core/rag/pipeline.py
- [X] T035 [US2] Implement content retrieval for selected-text context from Qdrant via RAGRetriever in chatbot/core/rag/retriever.py
- [X] T036 [US2] Test selected-text query functionality with sample content in test_selected_text_query.py
- [X] T037 [US2] Validate that responses are limited to selected text context via RAGValidator in chatbot/core/rag/validator.py

---

## Phase 5: User Story 3 - Verify Source Attribution (Priority: P3)

As a technical reader, I want to see clear source references for each answer so that I can verify the information and locate it in the original book.

**Independent Test**: Can be tested by examining responses to ensure they include proper source citations that link back to specific parts of the book content.

- [X] T038 [P] [US3] Enhance response model to include detailed source references in chatbot/core/models/response.py
- [X] T039 [US3] Update generator to include source references in responses in chatbot/core/rag/generator.py
- [X] T040 [US3] Enhance retriever to capture and return detailed source information in chatbot/core/rag/retriever.py
- [X] T041 [US3] Update API response format to include source reference details in chatbot/api/models/response.py and chatbot/api/routers/query.py
- [X] T042 [US3] Test source attribution functionality across all query types in test_source_attribution.py
- [X] T043 [US3] Validate that all responses contain accurate source references via the RAG retrieval process and validation in chatbot/core/rag/validator.py

---

## Phase 6: Polish & Cross-Cutting Concerns

Final implementation touches and system integration.

- [X] T044 Implement main FastAPI application in chatbot/api/main.py
- [X] T045 Add request/response logging and monitoring via chatbot/utils/logging.py and chatbot/utils/performance_monitor.py
- [X] T046 Implement error handling and graceful degradation via chatbot/utils/error_handlers.py
- [X] T047 Add performance monitoring for response times via chatbot/utils/performance_monitor.py
- [X] T048 Create API documentation with Swagger/OpenAPI in docs/api_documentation.md
- [X] T049 Test end-to-end functionality with complete book content in test_end_to_end.py
- [X] T050 Validate zero hallucination requirement across all user stories via RAGValidator in chatbot/core/rag/validator.py and validation in all query pathways
- [X] T051 Optimize for <2s response times as specified in requirements via performance monitoring in chatbot/utils/performance_monitor.py and response time tracking in main FastAPI application
- [X] T052 Create comprehensive test suite for all functionality in tests/test_rag_chatbot.py
- [X] T053 Document deployment instructions for free-tier compatibility in docs/deployment_guide.md