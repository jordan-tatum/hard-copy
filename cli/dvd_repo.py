"""
DVD repository functions using psycopg2.

This is your original dvd_repo.py - kept for reference.
The new API version is in app/routers/dvds.py
"""

from datetime import date
import pandas as pd
import re
from db import get_connection

def normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r'[^a-z0-9 ]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title


def insert_dvd(title: str, location: str) -> str:
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            return "Failed to connect to database."
        
        with conn.cursor() as cursor:
            # Check if movie already exists
            cursor.execute("SELECT title FROM dvds;")
            existing_titles = cursor.fetchall()
            
            norm_title = normalize_title(title)
            for (db_title,) in existing_titles:
                if normalize_title(db_title) == norm_title:
                    return "Movie already exists in your collection."
            
            # Insert the new DVD
            cursor.execute(
                "INSERT INTO dvds (title, purchase_location, purchase_date) VALUES (%s, %s, %s);",
                (title, location, date.today())
            )
            conn.commit()
        
        return f"'{title}' was successfully added to your collection."
    except Exception as e:
        if conn:
            conn.rollback()
        return f"Error inserting DVD: {e}"
    finally:
        if conn:
            conn.close()


def remove_dvd(title: str) -> str:
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            return "Failed to connect to database."
        
        with conn.cursor() as cursor:
            norm_title = normalize_title(title)
            cursor.execute("SELECT title FROM dvds;")
            all_titles = cursor.fetchall()
            
            original_title = None
            for (db_title,) in all_titles:
                if normalize_title(db_title) == norm_title:
                    original_title = db_title
                    break
            
            if not original_title:
                return f"'{title}' not found in collection."
            
            cursor.execute("DELETE FROM dvds WHERE title = %s;", (original_title,))
            conn.commit()
        
        return f"'{original_title}' has been removed from your collection."
    except Exception as e:
        if conn:
            conn.rollback()
        return f"Error removing DVD: {e}"
    finally:
        if conn:
            conn.close()


def get_all_dvds() -> pd.DataFrame:
    conn = None
    try:
        conn = get_connection()
        if conn is None:
            print("Failed to connect to database.")
            return pd.DataFrame()
        
        conn.autocommit = True
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM dvds ORDER BY purchase_date DESC;")
            rows = cursor.fetchall()
            colnames = [desc[0] for desc in cursor.description]
            
            if rows:
                df = pd.DataFrame(rows, columns=colnames)
            else:
                df = pd.DataFrame(columns=colnames)
            return df
            
    except Exception as e:
        print(f"Error fetching DVDs: {e}")
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()