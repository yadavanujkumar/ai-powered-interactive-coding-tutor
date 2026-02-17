from fastapi import FastAPI
from src.api.routes import router

app = FastAPI(title="AI-Powered Interactive Coding Tutor")

# Include API routes
app.include_router(router)
