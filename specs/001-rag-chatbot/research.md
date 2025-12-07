# Research: Integrated RAG Chatbot for Published Book

## API Keys and Configuration

### Qdrant Vector Database
```python
qdrant_client = QdrantClient(
    url="https://e55cfc43-4305-404e-9902-943e27319128.europe-west3-0.gcp.cloud.qdrant.io:6333",
    api_key="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.WiC3WupqiKbu_zXytQ5kzAQAj-0r05LVoiiZQEjUjRg",
)
```

### Cohere API
```
cohere_api_key=TBzr37EHlK7ZNCxtH8XcApXOJPyYbvB10IPGT6o8
```

### Neon Postgres Database
```
neon_db_url=napi_d1ng86bjx00aou8sw49vtgp6mt4d5g3f2xilxdbrkn3hncx9u9xs1td86bp4pgcr
```

### Google Gemini API
```
gemini_api_key=AIzaSyAvMXV0R3oSY5QO-HNRLNQuzWGpJEMA0Hw
```

## Decision: Technology Stack Selection

### Rationale:
Based on the feature requirements and provided API keys, the following technology stack has been selected:

1. **Qdrant** - Vector database for efficient similarity search of book content embeddings
2. **Cohere** - For text embeddings and potentially language model capabilities
3. **Neon Postgres** - For storing session metadata, conversation history, and user data
4. **Google Gemini** - Alternative LLM for response generation (in addition to OpenAI as mentioned in spec)
5. **FastAPI** - Backend framework for building the API with automatic documentation

### Alternatives Considered:
1. **Pinecone vs Qdrant**: Qdrant was chosen as it's provided in the requirements and offers free tier compatibility
2. **OpenAI vs Cohere vs Gemini**: Multiple LLM providers are available to provide flexibility and redundancy
3. **Traditional PostgreSQL vs Neon**: Neon was specified in the requirements for serverless Postgres capabilities

## Architecture Decisions

### Decision: Retrieval-Augmented Generation (RAG) Pipeline
- **Rationale**: The core requirement is to ensure all responses are grounded in book content with zero hallucination. RAG provides the perfect architecture for this by retrieving relevant content first, then generating responses based only on retrieved context.

### Decision: Embedding Strategy
- **Rationale**: Book content will be chunked and converted to embeddings for efficient retrieval. Cohere embeddings will be used initially, with the option to switch to OpenAI embeddings if needed.

### Decision: Content Processing Pipeline
- **Rationale**: Book content needs to be processed, chunked with appropriate metadata, and stored in the vector database. This will happen during an ingestion phase before queries can be processed.

## Reference Links
- Book Reference: https://ai-book-hackathon-two.vercel.app/
- Qdrant Cloud: QdrantClient with provided URL and API key
- Database: Neon Postgres with provided connection string