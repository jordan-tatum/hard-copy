"""
Database configuration and session management.

This replaces your old db.py with SQLAlchemy.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fix — no fallback, fails loudly if .env is missing
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found. Check your .env file.")


# ============================================================================
# DATABASE ENGINE
# ============================================================================

# Create SQLAlchemy engine
# The engine manages database connections and connection pooling
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True to see SQL queries in console
    pool_pre_ping=True,  # Verify connections before using them
    pool_size=5,  # Number of connections to keep open
    max_overflow=10  # Max connections beyond pool_size
)


# ============================================================================
# SESSION FACTORY
# ============================================================================

# SessionLocal creates database sessions for each request
SessionLocal = sessionmaker(
    autocommit=False,  # Require explicit commits
    autoflush=False,   # Don't auto-flush on queries
    bind=engine        # Bind to our engine
)


# ============================================================================
# BASE CLASS
# ============================================================================

# Base class for all SQLAlchemy models
# All your models (DVD, etc.) will inherit from this
Base = declarative_base()


# ============================================================================
# DEPENDENCY INJECTION
# ============================================================================

def get_db():
    """
    Database session dependency for FastAPI.
    
    This function:
    1. Creates a new database session
    2. Yields it to the endpoint
    3. Closes it when done (even if error occurs)
    
    Usage in endpoints:
        @app.get("/dvds")
        def get_dvds(db: Session = Depends(get_db)):
            dvds = db.query(DVD).all()
            return dvds
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def test_connection():
    """
    Test database connection.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        print("✅ Database connection successful!")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


if __name__ == "__main__":
    # Test connection when run directly
    print("Testing database connection...")
    test_connection()