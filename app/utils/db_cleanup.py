"""
Database maintenance utilities.

Converted from your db_utils.py to work with FastAPI/SQLAlchemy.
"""

from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Dict


def terminate_hanging_connections(
    db: Session,
    database_name: str = "movies"
) -> Dict[str, any]:
    """
    Terminate hanging database connections.
    
    Same functionality as your db_utils.py but using SQLAlchemy.
    
    Args:
        db: SQLAlchemy database session
        database_name: Name of the database (default: "movies")
    
    Returns:
        Dictionary with termination results
    
    Example usage:
        from app.database import SessionLocal
        from app.utils.db_cleanup import terminate_hanging_connections
        
        db = SessionLocal()
        result = terminate_hanging_connections(db)
        print(result)
        db.close()
    """
    try:
        # Execute the termination query
        result = db.execute(
            text("""
                SELECT pg_terminate_backend(pid) 
                FROM pg_stat_activity 
                WHERE datname = :db_name 
                AND pid <> pg_backend_pid()
            """),
            {"db_name": database_name}
        )
        
        # Count terminated connections
        count = sum(1 for row in result if row[0])
        
        return {
            "success": True,
            "terminated": count,
            "message": f"✓ Terminated {count} hanging connection(s)"
        }
    
    except Exception as e:
        return {
            "success": False,
            "terminated": 0,
            "message": f"✗ Error: {str(e)}"
        }


def check_active_connections(
    db: Session,
    database_name: str = "movies"
) -> Dict[str, any]:
    """
    Check active connections to the database.
    
    Args:
        db: SQLAlchemy database session
        database_name: Name of the database (default: "movies")
    
    Returns:
        Dictionary with connection information
    
    Example:
        result = check_active_connections(db)
        print(f"Active connections: {result['count']}")
    """
    try:
        result = db.execute(
            text("""
                SELECT pid, usename, application_name, state, query_start
                FROM pg_stat_activity 
                WHERE datname = :db_name
            """),
            {"db_name": database_name}
        )
        
        connections = []
        for row in result:
            connections.append({
                "pid": row[0],
                "user": row[1],
                "application": row[2],
                "state": row[3],
                "query_start": str(row[4])
            })
        
        return {
            "success": True,
            "count": len(connections),
            "connections": connections,
            "message": f"Found {len(connections)} active connection(s)"
        }
    
    except Exception as e:
        return {
            "success": False,
            "count": 0,
            "connections": [],
            "message": f"Error: {str(e)}"
        }


# ============================================================================
# STANDALONE SCRIPT USAGE
# ============================================================================

if __name__ == "__main__":
    """
    Run this file directly to clean up connections:
        python app/utils/db_cleanup.py
    """
    from app.database import SessionLocal
    
    print("=== Database Connection Cleanup ===\n")
    
    db = SessionLocal()
    
    try:
        # Check connections first
        print("Checking active connections...")
        check_result = check_active_connections(db)
        print(check_result["message"])
        
        if check_result["count"] > 0:
            print("\nActive connections:")
            for conn in check_result["connections"]:
                print(f"  PID: {conn['pid']} | User: {conn['user']} | State: {conn['state']}")
        
        # Terminate hanging connections
        print("\nTerminating hanging connections...")
        term_result = terminate_hanging_connections(db)
        print(term_result["message"])
        
        # Check again after cleanup
        print("\nRechecking connections...")
        check_result = check_active_connections(db)
        print(check_result["message"])
    
    finally:
        db.close()