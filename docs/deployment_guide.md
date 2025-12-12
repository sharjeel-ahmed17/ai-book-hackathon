# Deployment Guide: RAG Chatbot for Published Book

## Overview
This guide provides instructions for deploying the RAG Chatbot with free-tier compatible resources.

## Prerequisites
- Python 3.11+
- pip package manager
- Git
- Access to free-tier services (Qdrant Cloud, Neon Postgres, API keys)

## Architecture Overview
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Client Apps   │───▶│  FastAPI Server  │───▶│  Qdrant Vector  │
└─────────────────┘    └──────────────────┘    │    Database     │
                                              ├─────────────────┤
                                              │  Neon Postgres  │
                                              │   Metadata DB   │
                                              └─────────────────┘
```

## Environment Setup

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd ai-book-hackathon
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy the `.env.example` file and add your actual API keys:

```bash
cp .env.example .env
```

Edit `.env` with your API keys and service URLs:
```env
# Qdrant Configuration
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_api_key

# Cohere Configuration
COHERE_API_KEY=your_cohere_api_key

# Neon Postgres Configuration
NEON_DATABASE_URL=your_neon_db_url

# Google Gemini Configuration
GEMINI_API_KEY=your_gemini_api_key

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY=your_openai_api_key

# Application Settings
DEBUG=False
```

## Free-Tier Service Setup

### Qdrant Cloud Free Tier
1. Go to [Qdrant Cloud](https://qdrant.tech/)
2. Create an account and a free cluster
3. Note your cluster URL and API key
4. Update your `.env` file with these values

### Neon Serverless Postgres
1. Go to [Neon](https://neon.tech/)
2. Create an account and a new project
3. Get your connection string
4. Update your `.env` file with the connection string

### API Keys
1. **Cohere**: Sign up at [Cohere](https://dashboard.cohere.ai/) for embeddings
2. **Google Gemini**: Get API key from [Google AI Studio](https://makersuite.google.com/)
3. **OpenAI**: Get API key from [OpenAI Platform](https://platform.openai.com/) (optional)

## Running Locally

### 1. Start the Application
```bash
cd chatbot/api
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Access the API
- API Documentation: `http://localhost:8000/api/v1/docs`
- Health Check: `http://localhost:8000/api/v1/health`

### 3. Ingest Sample Content
```bash
curl -X POST http://localhost:8000/api/v1/ingest \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": "sample-book",
    "title": "Sample Book",
    "content": "This is sample book content for testing the RAG system..."
  }'
```

### 4. Query the Chatbot
```bash
curl -X POST http://localhost:8000/api/v1/query \
  -H "Content-Type: application/json" \
  -d '{
    "query": "What is this book about?",
    "context_type": "FULL_BOOK"
  }'
```

## Docker Deployment (Optional)

### 1. Build Docker Image
```bash
docker build -t rag-chatbot .
```

### 2. Run with Docker
```bash
docker run -d \
  --name rag-chatbot \
  --env-file .env \
  -p 8000:8000 \
  rag-chatbot
```

## Performance Optimization for Free Tier

### 1. Resource Management
- Limit concurrent requests to prevent hitting API rate limits
- Implement caching for frequent queries
- Use efficient embedding models to reduce costs

### 2. Query Optimization
- Limit query length to prevent excessive processing
- Implement timeouts to prevent hanging requests
- Cache embeddings to avoid regenerating them

### 3. Monitoring
- Monitor response times to ensure `<2s` performance
- Track API usage to stay within free tier limits
- Set up alerts for service degradation

## Scaling Considerations

### Horizontal Scaling
- Use a load balancer for multiple instances
- Ensure session affinity for consistent user experience
- Scale based on concurrent query volume

### Vertical Scaling
- Increase instance resources for complex queries
- Optimize database connections
- Tune embedding batch sizes

## Security Best Practices

### 1. API Key Management
- Never commit API keys to version control
- Use environment variables for sensitive data
- Rotate keys regularly

### 2. Input Validation
- Sanitize all user inputs
- Validate query lengths and content
- Implement rate limiting

### 3. Network Security
- Use HTTPS for all communications
- Restrict database access to application servers only
- Implement firewall rules

## Troubleshooting

### Common Issues

#### Issue: Connection Timeout
**Solution**: Check your network connection and API key validity
```bash
# Test Qdrant connection
curl -X GET "https://your-qdrant-url/collections" \
  -H "api-key: your-api-key"
```

#### Issue: Slow Response Times
**Solution**: Optimize queries and check resource usage
- Reduce query complexity
- Verify embeddings are properly cached
- Check database connection pooling

#### Issue: Memory Errors
**Solution**: Optimize batch processing and resource usage
- Reduce embedding batch sizes
- Implement proper garbage collection
- Monitor memory usage patterns

### Logging
- Enable DEBUG mode for detailed logs
- Check application logs for error details
- Monitor external service logs

## Monitoring and Maintenance

### Health Checks
Regularly check:
- API availability
- Database connectivity
- Vector database performance
- External service availability

### Performance Metrics
Track:
- Average response time
- Query success rate
- Error rates
- Resource utilization

## Cost Management

### Free Tier Limits
- Qdrant: Check monthly vector operations limit
- Neon Postgres: Monitor compute and storage usage
- API Services: Track token usage for embeddings/LLMs

### Optimization Tips
- Use efficient embedding models
- Implement result caching
- Batch operations where possible
- Monitor usage regularly

## Support and Community

For support:
- Check the GitHub repository for issues
- Review the documentation
- Contact the development team if needed

## Conclusion

This deployment guide provides the essential steps to deploy the RAG Chatbot with free-tier resources. Monitor your usage closely to stay within free tier limits, and consider upgrading services as your usage grows.