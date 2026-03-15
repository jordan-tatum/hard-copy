"""
DVD Tracker API - Main Application

This is the entry point for your FastAPI application.
Replaces your CLI main.py with a web API.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from .database import engine, Base
from .routers import dvds


# ============================================================================
# CREATE DATABASE TABLES
# ============================================================================

# Create all tables defined in models.py
# This runs when the app starts
Base.metadata.create_all(bind=engine)


# ============================================================================
# INITIALIZE FASTAPI APP
# ============================================================================

app = FastAPI(
    title="DVD Collection Tracker API",
    description="""
    A REST API for managing your DVD collection.
    
    ## Features
    
    * **Add DVDs** - Add new DVDs to your collection
    * **View Collection** - See all your DVDs
    * **Search** - Find DVDs by title
    * **Update** - Modify DVD information
    * **Delete** - Remove DVDs from collection
    
    ## Getting Started
    
    1. Visit `/docs` for interactive API documentation
    2. Try out the endpoints with the "Try it out" buttons
    3. Build your frontend to consume these endpoints
    """,
    version="2.0.0",
    contact={
        "name": "Jordan",
        "email": "your-email@example.com"
    },
    license_info={
        "name": "MIT"
    }
)


# ============================================================================
# CORS MIDDLEWARE
# ============================================================================

# Allow frontend to connect from different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React default
        "http://localhost:5173",  # Vite default
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5500",   # production front-end
        "http://localhost:5500",

    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)


# ============================================================================
# INCLUDE ROUTERS
# ============================================================================

# Include DVD router (all /api/dvds endpoints)
app.include_router(dvds.router)


# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get("/", include_in_schema=False)
async def root():
    """
    Root endpoint - redirects to API documentation.
    
    When someone visits http://localhost:8000/
    they get redirected to http://localhost:8000/docs
    """
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    """
    Health check endpoint.
    
    Useful for monitoring if API is running.
    Production tools can ping this endpoint.
    """
    return {
        "status": "healthy",
        "version": "2.0.0",
        "api": "DVD Collection Tracker"
    }


@app.get("/api")
async def api_root():
    """
    API root endpoint with available routes.
    
    Shows what endpoints are available.
    """
    return {
        "message": "DVD Collection Tracker API",
        "version": "2.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "dvds": "/api/dvds"
        },
        "documentation": "Visit /docs for interactive API documentation"
    }


# ============================================================================
# STARTUP/SHUTDOWN EVENTS
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """
    Runs when the API starts.
    
    Useful for:
    - Initializing database connections
    - Loading configuration
    - Starting background tasks
    """
    print("🚀 DVD Tracker API starting up...")
    print("📚 Database tables created/verified")
    print("✅ API ready to accept requests")


@app.on_event("shutdown")
async def shutdown_event():
    """
    Runs when the API shuts down.
    
    Useful for:
    - Closing database connections
    - Cleanup tasks
    - Saving state
    """
    print("👋 DVD Tracker API shutting down...")


# ============================================================================
# ERROR HANDLERS (Optional but recommended)
# ============================================================================

from fastapi import Request, status
from fastapi.responses import JSONResponse


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Custom 404 handler."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error": "Not Found",
            "message": f"The endpoint {request.url.path} does not exist",
            "hint": "Visit /docs to see available endpoints"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Custom 500 handler."""
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "An unexpected error occurred",
            "hint": "Please try again or contact support"
        }
    )


# ============================================================================
# DEVELOPMENT INFO
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("""
    ⚠️  Running directly with `python app/main.py` is not recommended.
    
    Instead, use one of these methods:
    
    1. Use the run script:
        python run.py
    
    2. Use uvicorn directly:
        uvicorn app.main:app --reload
    
    3. For production:
        uvicorn app.main:app --host 0.0.0.0 --port 8000
    """)
    
    # Run anyway for convenience
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )