# RAG Chatbot API Documentation

## Overview
The RAG Chatbot API provides endpoints for querying book content with zero hallucination. All responses are grounded in the provided book content with proper source attribution.

## Base URL
```
https://your-deployment-url.com/api/v1
```

## Authentication
This API does not require authentication for basic functionality, but you may implement authentication as needed.

## Endpoints

### Health Check
```
GET /health
```

Check the health status of the service.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-12-07T10:30:00Z",
  "service": "RAG Chatbot for Published Book",
  "version": "1.0.0",
  "dependencies": {
    "qdrant": "available",
    "postgres": "available",
    "embedding_service": "available"
  }
}
```

### Query Book Content
```
POST /query
```

Process a user query against the book content.

**Request Body:**
```json
{
  "query": "What are the main principles of RAG systems?",
  "context_type": "FULL_BOOK",
  "selected_text": "Optional text for selected-text queries",
  "session_id": "Optional session identifier"
}
```

**Parameters:**
- `query` (string, required): The user's question or query
- `context_type` (enum, required): "FULL_BOOK" or "SELECTED_TEXT"
- `selected_text` (string, optional): Specific text for selected-text context
- `session_id` (string, optional): Session identifier for conversation history

**Response:**
```json
{
  "response_id": "uuid-string",
  "answer": "The main principles of RAG systems include...",
  "source_references": [
    {
      "reference": "Chapter 3, Section 2, Page 45 (Page: 45) (Chapter: 3) (Section: 2)",
      "text": "Original text from the book that supports this answer",
      "relevance_score": 0.92,
      "page_number": 45,
      "chapter": "3",
      "section": "2",
      "content_id": "context-uuid"
    }
  ],
  "session_id": "session-uuid",
  "validation_status": "PASSED"
}
```

### Ingest Book Content
```
POST /ingest
```

Ingest book content for retrieval.

**Request Body:**
```json
{
  "book_id": "unique-book-identifier",
  "title": "Book Title",
  "content": "Full book content in markdown format",
  "metadata": {
    "author": "Author Name",
    "publication_date": "2023-01-01",
    "chapters": [
      {
        "chapter_number": 1,
        "title": "Introduction",
        "start_page": 1,
        "end_page": 20
      }
    ]
  }
}
```

**Response:**
```json
{
  "status": "success",
  "content_id": "uuid-of-ingested-content",
  "chunks_processed": 42,
  "processing_time_ms": 1250
}
```

## Error Responses

The API uses standard HTTP status codes:

- `200`: Success
- `400`: Bad Request - Invalid request format
- `422`: Unprocessable Entity - Query cannot be answered from book content
- `500`: Internal Server Error - Processing error

## Performance Metrics

The API includes performance monitoring with the following headers in responses:
- `X-Response-Time`: Time taken to process the request in milliseconds
- `X-Request-ID`: Unique identifier for the request

## Source Attribution

All responses include detailed source references with:
- Original text snippets
- Page numbers (when available)
- Chapter information
- Section information
- Relevance scores
- Content IDs

## Rate Limiting

The API does not include built-in rate limiting. Implement rate limiting at the infrastructure level as needed.

## Security

- All API keys are stored in environment variables
- Input validation is performed on all endpoints
- SQL injection is prevented through ORM usage
- XSS protection is provided through proper output encoding

## Free-tier Compatibility

The implementation is designed to work with free-tier resources:
- Qdrant Cloud Free Tier
- Neon Serverless Postgres
- Minimal resource usage
- Efficient caching where possible