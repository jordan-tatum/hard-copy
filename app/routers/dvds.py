"""
DVD API Routes

This file contains all DVD-related endpoints.
Converts your dvd_repo.py functions into REST API endpoints.
"""

from fastapi import APIRouter, Depends, HTTPException, status, Response, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import date
from typing import List, Optional
import re

from ..database import get_db
from ..models import DVD
from ..schemas import DVDCreate, DVDResponse, DVDUpdate, DVDList, Message


# ============================================================================
# ROUTER SETUP
# ============================================================================

router = APIRouter(
    prefix="/api/dvds",
    tags=["DVDs"],
    redirect_slashes=False,
    responses={
        404: {"description": "DVD not found"},
        400: {"description": "Bad request"}
    }
)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def normalize_title(title: str) -> str:
    """
    Normalize DVD title for duplicate checking.
    
    Same logic as your dvd_repo.py normalize_title function.
    Removes special characters, extra spaces, and converts to lowercase.
    
    Examples:
        "The Matrix!" → "the matrix"
        "Star  Wars" → "star wars"
        "IT (2017)" → "it 2017"
    """
    title = title.lower()
    title = re.sub(r'[^a-z0-9 ]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title


def check_duplicate(db: Session, title: str, exclude_id: Optional[int] = None) -> Optional[DVD]:
    """
    Check if DVD with similar title already exists.
    
    Args:
        db: Database session
        title: Title to check
        exclude_id: DVD ID to exclude (for updates)
    
    Returns:
        Existing DVD if found, None otherwise
    """
    normalized_new = normalize_title(title)
    
    query = db.query(DVD)
    if exclude_id:
        query = query.filter(DVD.id != exclude_id)
    
    all_dvds = query.all()
    
    for dvd in all_dvds:
        if normalize_title(dvd.title) == normalized_new:
            return dvd
    
    return None


# ============================================================================
# API ENDPOINTS
# ============================================================================

@router.get("/", response_model=List[DVDResponse], summary="Get all DVDs")
def get_all_dvds(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Max number of records to return"),
    sort_by: str = Query("purchase_date", description="Field to sort by"),
    order: str = Query("desc", description="Sort order: asc or desc")
):
    """
    Retrieve all DVDs in the collection.
    
    **Replaces:** `get_all_dvds()` from dvd_repo.py
    
    **Your old code:**
```python
    df = pd.read_sql("SELECT * FROM dvds;", conn)
    return df
```
    
    **New SQLAlchemy code:**
```python
    dvds = db.query(DVD).all()
    return dvds
```
    
    **Query Parameters:**
    - `skip`: Pagination offset (default: 0)
    - `limit`: Max results to return (default: 100)
    - `sort_by`: Field to sort by (default: purchase_date)
    - `order`: Sort direction - "asc" or "desc" (default: desc)
    
    **Examples:**
    - Get all DVDs: `/api/dvds`
    - Get first 10: `/api/dvds?limit=10`
    - Sort by title: `/api/dvds?sort_by=title&order=asc`
    - Pagination: `/api/dvds?skip=20&limit=10` (page 3)
    """
    # Build query
    query = db.query(DVD)
    
    # Apply sorting
    if hasattr(DVD, sort_by):
        sort_column = getattr(DVD, sort_by)
        if order.lower() == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
    else:
        # Default sort
        query = query.order_by(DVD.purchase_date.desc())
    
    # Apply pagination
    dvds = query.offset(skip).limit(limit).all()
    
    return dvds


@router.get("/count", response_model=dict, summary="Get DVD count")
def get_dvd_count(db: Session = Depends(get_db)):
    """
    Get total number of DVDs in collection.
    
    Useful for displaying collection size.
    
    **Returns:**
```json
    {
        "total": 42,
        "message": "You have 42 DVDs in your collection"
    }
```
    """
    count = db.query(DVD).count()
    return {
        "total": count,
        "message": f"You have {count} DVD{'s' if count != 1 else ''} in your collection"
    }


@router.get("/search", response_model=List[DVDResponse], summary="Search DVDs")
def search_dvds(
    title: str = Query(..., min_length=1, description="Search term"),
    db: Session = Depends(get_db)
):
    """
    Search for DVDs by title (partial match, case-insensitive).
    
    **New feature** - didn't exist in CLI version!
    
    **Examples:**
    - Search for "matrix": `/api/dvds/search?title=matrix`
    - Search for "star": `/api/dvds/search?title=star`
    
    **Returns:** List of DVDs matching the search term
    """
    # Case-insensitive partial match
    dvds = db.query(DVD).filter(
        DVD.title.ilike(f"%{title}%")
    ).order_by(DVD.title).all()
    
    return dvds


@router.get("/{id}", response_model=DVDResponse, summary="Get DVD by ID")
def get_dvd(id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific DVD by ID.
    
    **New endpoint** - useful for frontend to fetch single DVD details.
    
    **Path Parameters:**
    - `id`: DVD ID (integer)
    
    **Example:** `/api/dvds/5` returns DVD with ID 5
    
    **Returns:** DVD details or 404 if not found
    """
    dvd = db.query(DVD).filter(DVD.id == id).first()
    
    if not dvd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DVD with id {id} not found in collection"
        )
    
    return dvd


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=DVDResponse,
    summary="Add new DVD"
)
def create_dvd(dvd: DVDCreate, db: Session = Depends(get_db)):
    """
    Add a new DVD to the collection.
    
    **Replaces:** `insert_dvd(title, location)` from dvd_repo.py
    
    **Your old code:**
```python
    cursor.execute(
        "INSERT INTO dvds (title, purchase_location, purchase_date) VALUES (%s, %s, %s);",
        (title, location, date.today())
    )
    conn.commit()
```
    
    **New SQLAlchemy code:**
```python
    new_dvd = DVD(title=..., purchase_location=..., purchase_date=date.today())
    db.add(new_dvd)
    db.commit()
```
    
    **Request Body:**
```json
    {
        "title": "The Matrix"",
        "purchase_location": "Best Buy"
        }
**Improvements over CLI:**
    - Automatic duplicate detection
    - Better error messages
    - Returns the created DVD with ID
    - Input validation
    
    **Returns:** The newly created DVD with auto-generated ID and date
    """
    # Check for duplicates using your normalize_title logic
    existing = check_duplicate(db, dvd.title)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"DVD '{dvd.title}' already exists in collection (ID: {existing.id})"
        )
    
    # Create new DVD with today's date
    new_dvd = DVD(
        title=dvd.title,
        purchase_location=dvd.purchase_location,
        purchase_date=date.today()
    )
    
    # Add to database
    db.add(new_dvd)
    db.commit()
    db.refresh(new_dvd)  # Get the auto-generated ID
    
    return new_dvd


@router.put("/{id}", response_model=DVDResponse, summary="Update DVD")
def update_dvd(id: int, dvd: DVDUpdate, db: Session = Depends(get_db)):
    """
    Update an existing DVD.
    
    **New endpoint** - allows editing DVD information!
    Your wife can fix typos or update purchase location.
    
    **Path Parameters:**
    - `id`: DVD ID to update
    
    **Request Body** (all fields optional):
```json
    {
        "title": "The Matrix Reloaded",
        "purchase_location": "Amazon",
        "purchase_date": "2025-12-25"
    }
```
    
    **Features:**
    - Only updates fields that are provided
    - Checks for duplicate titles (excluding current DVD)
    - Returns updated DVD
    
    **Example:** Update just the title:
```json
    {
        "title": "New Title"
    }
```
    """
    # Find the DVD
    dvd_query = db.query(DVD).filter(DVD.id == id)
    existing_dvd = dvd_query.first()
    
    if not existing_dvd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DVD with id {id} not found"
        )
    
    # Check for duplicate title if title is being updated
    if dvd.title and dvd.title != existing_dvd.title:
        duplicate = check_duplicate(db, dvd.title, exclude_id=id)
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"DVD '{dvd.title}' already exists (ID: {duplicate.id})"
            )
    
    # Update only provided fields
    update_data = dvd.model_dump(exclude_unset=True)
    
    if update_data:  # Only update if there's something to update
        dvd_query.update(update_data, synchronize_session=False)
        db.commit()
        db.refresh(existing_dvd)
    
    return existing_dvd


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete DVD")
def delete_dvd(id: int, db: Session = Depends(get_db)):
    """
    Remove a DVD from the collection.
    
    **Replaces:** `remove_dvd(title)` from dvd_repo.py
    
    **Your old code:**
```python
    cursor.execute("DELETE FROM dvds WHERE title = %s;", (original_title,))
    conn.commit()
```
    
    **New SQLAlchemy code:**
```python
    db.query(DVD).filter(DVD.id == id).delete()
    db.commit()
```
    
    **Improvement:** Uses ID instead of title (more reliable, handles duplicates better)
    
    **Path Parameters:**
    - `id`: DVD ID to delete
    
    **Example:** `/api/dvds/5` deletes DVD with ID 5
    
    **Returns:** 204 No Content on success, 404 if DVD not found
    """
    dvd_query = db.query(DVD).filter(DVD.id == id)
    dvd = dvd_query.first()
    
    if not dvd:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DVD with id {id} not found"
        )
    
    # Store title for potential logging
    deleted_title = dvd.title
    
    # Delete the DVD
    dvd_query.delete(synchronize_session=False)
    db.commit()
    
    # 204 responses should have no body
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/location/{location}", response_model=List[DVDResponse], summary="Get DVDs by location")
def get_dvds_by_location(location: str, db: Session = Depends(get_db)):
    """
    Get all DVDs purchased from a specific location.
    
    **New feature** - filter by purchase location!
    
    **Path Parameters:**
    - `location`: Purchase location (case-insensitive)
    
    **Example:** `/api/dvds/location/Best%20Buy`
    
    **Returns:** List of DVDs from that location
    """
    dvds = db.query(DVD).filter(
        DVD.purchase_location.ilike(f"%{location}%")
    ).order_by(DVD.purchase_date.desc()).all()
    
    return dvds


@router.get("/stats/summary", response_model=dict, summary="Get collection statistics")
def get_statistics(db: Session = Depends(get_db)):
    """
    Get statistics about your DVD collection.
    
    **New feature** - collection insights!
    
    **Returns:**
```json
    {
        "total_dvds": 42,
        "locations": {
            "Best Buy": 15,
            "Amazon": 20,
            "Target": 7
        },
        "recent_additions": [...],
        "oldest_dvd": {...},
        "newest_dvd": {...}
    }
```
    """
    total = db.query(DVD).count()
    
    # Get all DVDs for processing
    all_dvds = db.query(DVD).all()
    
    # Count by location
    locations = {}
    for dvd in all_dvds:
        loc = dvd.purchase_location or "Unknown"
        locations[loc] = locations.get(loc, 0) + 1
    
    # Get oldest and newest
    oldest = db.query(DVD).order_by(DVD.purchase_date.asc()).first()
    newest = db.query(DVD).order_by(DVD.purchase_date.desc()).first()
    
    # Recent additions (last 5)
    recent = db.query(DVD).order_by(DVD.purchase_date.desc()).limit(5).all()
    
    return {
        "total_dvds": total,
        "locations": locations,
        "recent_additions": [{"id": d.id, "title": d.title, "date": d.purchase_date} for d in recent],
        "oldest_dvd": {"id": oldest.id, "title": oldest.title, "date": oldest.purchase_date} if oldest else None,
        "newest_dvd": {"id": newest.id, "title": newest.title, "date": newest.purchase_date} if newest else None
    }


# ============================================================================
# COMPARISON: OLD (CLI) vs NEW (API)
# ============================================================================
"""
GET ALL DVDS:
-------------
OLD (dvd_repo.py):
    def get_all_dvds() -> pd.DataFrame:
        df = pd.read_sql("SELECT * FROM dvds;", conn)
        return df

NEW (API):
    @router.get("/", response_model=List[DVDResponse])
    def get_all_dvds(db: Session = Depends(get_db)):
        dvds = db.query(DVD).all()
        return dvds


ADD DVD:
--------
OLD (dvd_repo.py):
    def insert_dvd(title: str, location: str) -> str:
        cursor.execute(
            "INSERT INTO dvds (...) VALUES (%s, %s, %s);",
            (title, location, date.today())
        )
        conn.commit()
        return f"'{title}' was successfully added"

NEW (API):
    @router.post("/", status_code=201)
    def create_dvd(dvd: DVDCreate, db: Session = Depends(get_db)):
        new_dvd = DVD(title=dvd.title, ...)
        db.add(new_dvd)
        db.commit()
        return new_dvd


DELETE DVD:
-----------
OLD (dvd_repo.py):
    def remove_dvd(title: str) -> str:
        cursor.execute("DELETE FROM dvds WHERE title = %s;", (title,))
        conn.commit()
        return f"'{title}' has been removed"

NEW (API):
    @router.delete("/{id}", status_code=204)
    def delete_dvd(id: int, db: Session = Depends(get_db)):
        db.query(DVD).filter(DVD.id == id).delete()
        db.commit()
        return Response(status_code=204)


KEY IMPROVEMENTS:
-----------------
✅ Web accessible (your wife can use from phone)
✅ Better error handling
✅ Input validation (Pydantic)
✅ Search and filter capabilities
✅ Statistics and insights
✅ RESTful design
✅ Automatic API documentation
✅ Type safety
✅ More maintainable code
"""