# Data Model: Integrated RAG Chatbot for Published Book

## Entity: Query
- **Description**: A user's question or request for information from the book content, including context about whether to search full book or selected text
- **Fields**:
  - query_id (string, UUID): Unique identifier for the query
  - session_id (string, UUID): Reference to the conversation session
  - content (string): The actual question or query text from the user
  - context_type (enum): Type of context to search (FULL_BOOK or SELECTED_TEXT)
  - selected_text (string, optional): Specific text provided by user for selected-text queries
  - timestamp (datetime): When the query was submitted
  - source_references (array): List of source references for retrieved context

## Entity: Retrieved Context
- **Description**: Book content segments retrieved by the system as relevant to a user query, with source attribution
- **Fields**:
  - context_id (string, UUID): Unique identifier for the retrieved context
  - query_id (string, UUID): Reference to the original query
  - content_chunks (array of objects): Array of content chunks retrieved
    - text (string): The actual content text
    - source_reference (string): Where in the book this content appears
    - relevance_score (float): How relevant this chunk is to the query
  - metadata (object): Additional metadata about the retrieval
    - retrieval_method (string): How the content was retrieved
    - confidence_score (float): Confidence in the relevance of retrieved content

## Entity: Response
- **Description**: The chatbot's answer to a user query, grounded in retrieved book content with source references
- **Fields**:
  - response_id (string, UUID): Unique identifier for the response
  - query_id (string, UUID): Reference to the original query
  - content (string): The chatbot's response to the user
  - source_references (array): List of source references used in generating the response
  - timestamp (datetime): When the response was generated
  - validation_status (enum): Status of hallucination check (PASSED, FAILED, PENDING)

## Entity: Conversation Session
- **Description**: User interaction history stored in database for context preservation
- **Fields**:
  - session_id (string, UUID): Unique identifier for the session
  - user_id (string, optional): Identifier for the user (if authenticated)
  - created_at (datetime): When the session was created
  - last_activity (datetime): When the last interaction occurred
  - queries (array of objects): List of queries in this session
    - query_id (string): Reference to query entity
    - timestamp (datetime): When the query was made
  - metadata (object): Additional session metadata

## Entity: Book Content
- **Description**: The book content that will be used for retrieval and response generation
- **Fields**:
  - content_id (string, UUID): Unique identifier for the content chunk
  - book_id (string): Identifier for the book
  - title (string): Title of the content section/chapter
  - content_text (string): The actual text content
  - metadata (object): Additional metadata about the content
    - chapter_number (integer, optional): Chapter number if applicable
    - page_number (integer, optional): Page number if applicable
    - section_title (string, optional): Title of the section
    - tags (array of strings): Tags for categorization
  - embedding_vector (array of floats): Vector representation for similarity search
  - source_reference (string): Where in the book this content appears

## Entity: User Session Preference
- **Description**: User preferences for the current session (optional)
- **Fields**:
  - preference_id (string, UUID): Unique identifier for the preference
  - session_id (string, UUID): Reference to the session
  - query_context_default (enum): Default context type for queries (FULL_BOOK or SELECTED_TEXT)
  - response_format (enum): Preferred response format
  - source_citation_preference (boolean): Whether to always show source citations
  - created_at (datetime): When preferences were set
  - updated_at (datetime): When preferences were last updated

## Relationships
- Conversation Session (1) → Query (Many): One session can contain many queries
- Query (1) → Retrieved Context (1): Each query has one set of retrieved context
- Query (1) → Response (1): Each query generates one response
- Retrieved Context (1) → Book Content (Many): Retrieved context references multiple content chunks
- User Session Preference (1) → Conversation Session (1): One preference set per session