from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Qdrant settings
    qdrant_url: str = "https://e55cfc43-4305-404e-9902-943e27319128.europe-west3-0.gcp.cloud.qdrant.io:6333"
    qdrant_api_key: Optional[str] = None

    # Cohere settings
    cohere_api_key: Optional[str] = None

    # Neon Postgres settings
    neon_database_url: Optional[str] = None

    # Google Gemini settings
    gemini_api_key: Optional[str] = None

    # OpenAI settings
    openai_api_key: Optional[str] = None

    # Application settings
    app_name: str = "RAG Chatbot for Published Book"
    api_v1_prefix: str = "/api/v1"
    debug: bool = False
    max_query_length: int = 1000
    max_response_length: int = 2000
    response_timeout_seconds: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'


settings = Settings()