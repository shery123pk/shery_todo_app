"""
FastAPI Main Application

Professional Multi-Tenant Project Management System Backend API
Author: Sharmeen Asif
"""

from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from app.config import settings


# Initialize FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Professional multi-tenant project management system API",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Configure CORS
allowed_origins = settings.get_allowed_origins()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,  # Required for HttpOnly cookies
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Exception Handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle Pydantic validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "body": exc.body,
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": str(exc) if settings.debug else "An error occurred",
        },
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
        Response: {"status": "healthy", "service": "project-management-api"}
    """
    return {
        "status": "healthy",
        "service": "project-management-api",
        "version": settings.app_version,
        "environment": settings.environment,
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
        "message": "Project Management System API",
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }


# Lifecycle events
@app.on_event("startup")
async def startup_event():
    """
    Application startup event.
    Runs when the FastAPI app starts.
    """
    print(f"[STARTUP] {settings.app_name} v{settings.app_version} starting...")
    print(f"[ENV] Environment: {settings.environment}")
    print(f"[CORS] CORS enabled for: {', '.join(allowed_origins[:3])}...")

    # Initialize database (development only)
    if settings.debug:
        from app.database import init_db
        await init_db()
        print("[DB] Database tables created (development mode)")

    # Start email reminder service in background
    import asyncio
    from app.services.reminder_checker import start_reminder_service
    asyncio.create_task(start_reminder_service())
    print("[REMINDER SERVICE] Background email reminder service started")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event.
    Runs when the FastAPI app stops.
    """
    print(f"[SHUTDOWN] {settings.app_name} shutting down...")


# API Routers (will be added as we implement user stories)
# Phase 3 (User Story 7): Authentication
from app.routers import auth
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# Phase 4 (User Story 1): Organizations
# from app.routers import organizations, invitations
# app.include_router(organizations.router, prefix="/api/organizations", tags=["Organizations"])
# app.include_router(invitations.router, prefix="/api/invitations", tags=["Invitations"])

# Phase 5 (User Story 2): Projects
# from app.routers import projects
# app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])

# Phase 6 (User Story 3): Tasks
from app.routers import tasks
app.include_router(tasks.router, prefix="/api/tasks", tags=["Tasks"])

# Phase 3 (AI Integration): Chatbot
from app.routers import chatbot
app.include_router(chatbot.router, tags=["Chatbot"])
