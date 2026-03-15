"""
Database configuration and connection utilities for the DVD collection app.
Uses psycopg2 directly; no SQLAlchemy.

This is your original db.py file - kept for reference.
"""

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "movies")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")

if not DB_PASSWORD:
    raise ValueError("DB_PASSWORD not found. Check your .env file.")

def get_connection():
    """
    Create and return a psycopg2 PostgreSQL connection.
    """
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            connect_timeout=2  # Reduced from 5
        )
        return conn
    except psycopg2.OperationalError as e:
        print("Failed to connect to database:", e)
        return None