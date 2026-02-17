"""FastAPI application setup for AI-Powered Interactive Coding Tutor."""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.routes import router
from src.core.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.debug else logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    AI-Powered Interactive Coding Tutor API
    
    This API provides AI-powered tutoring services for learning programming.
    Features include:
    - Ask coding questions and receive detailed explanations
    - Submit code for review and feedback
    - Maintain conversation history for context-aware responses
    - Track learning progress through sessions
    """,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

logger.info(f"{settings.app_name} v{settings.app_version} initialized")


@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    logger.info("Application starting up...")
    logger.info(f"Using OpenAI model: {settings.openai_model}")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown."""
    logger.info("Application shutting down...")
