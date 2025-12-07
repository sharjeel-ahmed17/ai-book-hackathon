from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os
import uuid

from chatbot.config.settings import settings
from chatbot.api.routers import health, query, ingest
from chatbot.utils.error_handlers import add_error_handlers
from chatbot.utils.performance_monitor import performance_monitor_middleware, perf_monitor
from chatbot.utils.logging import APILogger


# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    FastAPI lifespan event handler for startup and shutdown events
    """
    # Startup
    logger.info(f"Starting {settings.app_name} API server")
    logger.info(f"Environment: {'development' if settings.debug else 'production'}")

    # Initialize services if needed
    # For example, verify database connections, load models, etc.

    yield  # Application runs here

    # Shutdown
    logger.info(f"Shutting down {settings.app_name} API server")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="A RAG (Retrieval-Augmented Generation) chatbot for querying published book content",
    version="1.0.0",
    docs_url=f"{settings.api_v1_prefix}/docs",
    redoc_url=f"{settings.api_v1_prefix}/redoc",
    lifespan=lifespan
)

# Add custom middleware for request ID, logging, and performance monitoring
@app.middleware("http")
async def add_request_id(request, call_next):
    """Add a unique request ID to each request"""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response

# Add performance monitoring middleware
app.middleware("http")(performance_monitor_middleware(app))

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handlers
add_error_handlers(app)

# Include API routers
app.include_router(health.router, prefix=settings.api_v1_prefix, tags=["health"])
app.include_router(query.router, prefix=settings.api_v1_prefix, tags=["query"])
app.include_router(ingest.router, prefix=settings.api_v1_prefix, tags=["ingest"])


# Include the root path to show API information
@app.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": "1.0.0",
        "endpoints": {
            "docs": f"{settings.api_v1_prefix}/docs",
            "health": f"{settings.api_v1_prefix}/health",
            "query": f"{settings.api_v1_prefix}/query",
            "ingest": f"{settings.api_v1_prefix}/ingest"
        }
    }


# Add additional middleware for logging, rate limiting, etc. if needed
@app.middleware("http")
async def add_process_time_header(request, call_next):
    import time
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "chatbot.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info" if not settings.debug else "debug"
    )