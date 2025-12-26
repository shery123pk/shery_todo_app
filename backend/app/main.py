"""
FastAPI Main Application
Phase 2 Full-Stack Web Todo Backend API
Author: Sharmeen Asif
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Todo application backend API with authentication",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
allowed_origins = settings.get_allowed_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,  # Required for httpOnly cookies
    allow_methods=["GET", "POST", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Health check endpoint
@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint for monitoring and deployment verification.

    Returns:
        dict: Service status and name

    Example:
        GET /health
        Response: {"status": "healthy", "service": "todo-backend"}
    """
    return {
        "status": "healthy",
        "service": "todo-backend",
        "version": settings.app_version,
        "environment": settings.environment
    }


# Root endpoint
@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint providing API information.

    Returns:
        dict: Welcome message and API details
    """
    return {
        "message": "Todo Backend API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health"
    }


# Lifecycle events
@app.on_event("startup")
async def startup_event():
    """
    Application startup event.
    Runs when the FastAPI app starts.
    """
    print(f"🚀 {settings.app_name} v{settings.app_version} starting...")
    print(f"📝 Environment: {settings.environment}")
    print(f"🔒 CORS enabled for: {', '.join(allowed_origins)}")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event.
    Runs when the FastAPI app stops.
    """
    print(f"👋 {settings.app_name} shutting down...")


# API Routers
from app.routers import auth, tasks, chatbot

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])
app.include_router(chatbot.router, tags=["Chatbot"])
