# Quickstart Guide: Integrated RAG Chatbot for Published Book

## Overview
This guide provides instructions to quickly set up and run the RAG Chatbot for querying published book content.

## Prerequisites
- Python 3.11+
- pip package manager
- Access to the provided API keys for Qdrant, Cohere, Neon Postgres, and Google Gemini

## Setup Steps

### 1. Clone and Navigate to Project
```bash
git clone <repository-url>
cd ai-book-hackathon
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install fastapi uvicorn qdrant-client cohere psycopg2-binary python-dotenv
```

### 4. Configure Environment Variables
Create a `.env` file in the project root with the following:
```
QDRANT_URL=https://e55cfc43-4305-404e-9902-943e27319128.europe-west3-0.gcp.cloud.qdrant.io:6333
QDRANT_API_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.WiC3WupqiKbu_zXytQ5kzAQAj-0r05LVoiiZQEjUjRg
COHERE_API_KEY=TBzr37EHlK7ZNCxtH8XcApXOJPyYbvB10IPGT6o8
NEON_DB_URL=napi_d1ng86bjx00aou8sw49vtgp6mt4d5g3f2xilxdbrkn3hncx9u9xs1td86bp4pgcr
GEMINI_API_KEY=AIzaSyAvMXV0R3oSY5QO-HNRLNQuzWGpJEMA0Hw
```

### 5. Start the API Server
```bash
cd chatbot/api
uvicorn main:app --reload --port 8000
```

## Basic Usage

### 1. Ingest Book Content
```bash
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "my-book-id",
    "title": "My Book Title",
    "content": "Full content of the book...",
    "metadata": {}
  }'
```

### 2. Query the Chatbot
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What are the main concepts in this book?",
    "context_type": "FULL_BOOK"
  }'
```

### 3. Check Health
```bash
curl http://localhost:8000/api/v1/health
```

## Key Components

### Project Structure
```
chatbot/
├── api/                 # FastAPI application
├── core/                # Core RAG logic
│   ├── rag/             # Retrieval and generation
│   ├── embeddings/      # Embedding processing
│   └── storage/         # Database integrations
├── services/            # Business logic services
└── utils/               # Utility functions
```

### Main Features
1. **Content Grounding**: All responses are grounded in book content with zero hallucination
2. **Source Attribution**: Every response includes source references
3. **Flexible Querying**: Support for both full-book and selected-text queries
4. **Fast Retrieval**: Vector database for efficient content retrieval

## Next Steps
1. Integrate with the book content from https://ai-book-hackathon-two.vercel.app/
2. Implement proper error handling and logging
3. Add authentication if needed for your use case
4. Set up monitoring and performance metrics