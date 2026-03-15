"""
SQLAlchemy database models.

Converts your PostgreSQL tables into Python classes.
"""

from sqlalchemy import Column, Integer, String, Date, Boolean, Text
from sqlalchemy.sql import func
from .database import Base


class DVD(Base):
    """
    DVD model - represents your 'dvds' table.
    
    This replaces direct SQL queries with Python objects.
    
    Your original table:
        CREATE TABLE dvds (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            purchase_date DATE,
            purchase_location TEXT
        );
    
    SQLAlchemy equivalent:
        This class definition below
    """
    
    __tablename__ = "dvds"
    
    # Primary key - auto-incrementing ID
    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        index=True  # Create index for faster lookups
    )
    
    # DVD title - required field
    title = Column(
        Text,
        nullable=False,
        index=True  # Index for faster title searches
    )
    
    # Purchase date - defaults to today
    purchase_date = Column(
        Date,
        nullable=False,
        server_default=func.current_date()  # Database-side default
    )
    
    # Purchase location - optional
    purchase_location = Column(
        Text,
        nullable=True
    )
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<DVD(id={self.id}, title='{self.title}', date={self.purchase_date})>"
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "purchase_date": self.purchase_date,
            "purchase_location": self.purchase_location
        }


# ============================================================================
# FUTURE MODELS (Examples for expansion)
# ============================================================================

# Uncomment and modify when you want to add these features:

# class Genre(Base):
#     """Genre model for categorizing DVDs."""
#     __tablename__ = "genres"
#     
#     id = Column(Integer, primary_key=True)
#     name = Column(String(50), unique=True, nullable=False)


# class DVDGenre(Base):
#     """Many-to-many relationship between DVDs and Genres."""
#     __tablename__ = "dvd_genres"
#     
#     dvd_id = Column(Integer, ForeignKey("dvds.id"), primary_key=True)
#     genre_id = Column(Integer, ForeignKey("genres.id"), primary_key=True)


# class WatchHistory(Base):
#     """Track when DVDs were watched."""
#     __tablename__ = "watch_history"
#     
#     id = Column(Integer, primary_key=True)
#     dvd_id = Column(Integer, ForeignKey("dvds.id"))
#     watched_date = Column(Date, default=func.current_date())
#     rating = Column(Integer)  # 1-5 stars
#     notes = Column(Text)