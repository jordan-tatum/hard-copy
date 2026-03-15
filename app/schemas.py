"""
Pydantic schemas for request/response validation.

These define what data looks like coming in and going out of your API.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import date
from typing import Optional


# ============================================================================
# BASE SCHEMAS
# ============================================================================

class DVDBase(BaseModel):
    """
    Base DVD schema with common fields.
    
    Other schemas inherit from this to avoid repetition.
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="DVD title",
        examples=["The Matrix"]
    )
    purchase_location: Optional[str] = Field(
        None,
        max_length=200,
        description="Where the DVD was purchased",
        examples=["Best Buy", "Amazon", "Target"]
    )


# ============================================================================
# REQUEST SCHEMAS
# ============================================================================

class DVDCreate(DVDBase):
    """
    Schema for creating a new DVD.
    
    Used when someone POSTs to /api/dvds
    
    Example request body:
        {
            "title": "The Matrix",
            "purchase_location": "Best Buy"
        }
    
    Note: purchase_date is auto-generated, so not included here
    """
    pass  # Inherits everything from DVDBase


class DVDUpdate(BaseModel):
    """
    Schema for updating a DVD.
    
    Used when someone PUTs to /api/dvds/{id}
    
    All fields are optional - only update what's provided.
    
    Example request body (updating only title):
        {
            "title": "The Matrix Reloaded"
        }
    """
    title: Optional[str] = Field(
        None,
        min_length=1,
        max_length=500,
        description="Updated DVD title"
    )
    purchase_location: Optional[str] = Field(
        None,
        max_length=200,
        description="Updated purchase location"
    )
    purchase_date: Optional[date] = Field(
        None,
        description="Updated purchase date"
    )


# ============================================================================
# RESPONSE SCHEMAS
# ============================================================================

class DVDResponse(DVDBase):
    """
    Schema for DVD responses.
    
    Used when API returns DVD data to client.
    Includes all fields including auto-generated ones.
    
    Example response:
        {
            "id": 1,
            "title": "The Matrix",
            "purchase_date": "2025-12-29",
            "purchase_location": "Best Buy"
        }
    """
    id: int = Field(..., description="Unique DVD identifier")
    purchase_date: date = Field(..., description="Date DVD was added to collection")
    
    # Configuration for Pydantic v2
    model_config = ConfigDict(from_attributes=True)


class DVDList(BaseModel):
    """
    Schema for list of DVDs with metadata.
    
    Useful for pagination in the future.
    """
    dvds: list[DVDResponse]
    total: int = Field(..., description="Total number of DVDs")
    
    model_config = ConfigDict(from_attributes=True)


# ============================================================================
# UTILITY SCHEMAS
# ============================================================================

class Message(BaseModel):
    """Generic message response."""
    message: str
    detail: Optional[str] = None


class ErrorResponse(BaseModel):
    """Error response schema."""
    error: str
    detail: str
    status_code: int


# ============================================================================
# SCHEMA USAGE EXAMPLES
# ============================================================================
"""
Request Validation (Automatic):
-------------------------------
@app.post("/api/dvds")
def create_dvd(dvd: DVDCreate):  # ← FastAPI validates against DVDCreate
    # If validation fails, FastAPI returns 422 error automatically
    # If validation passes, dvd is a valid DVDCreate object
    pass


Response Validation (Automatic):
--------------------------------
@app.get("/api/dvds", response_model=list[DVDResponse])
def get_dvds():
    dvds = db.query(DVD).all()  # Returns SQLAlchemy DVD objects
    return dvds  # FastAPI converts to DVDResponse automatically


Benefits:
---------
✅ Automatic validation (no manual checking)
✅ Automatic documentation (shows in /docs)
✅ Type safety (IDE autocomplete)
✅ Clear API contracts (frontend knows what to expect)
✅ Automatic error messages (user-friendly validation errors)
"""