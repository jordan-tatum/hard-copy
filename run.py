"""
Quick start script for DVD Tracker API.

Run this file to start the API server:
    python run.py
"""

import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

if __name__ == "__main__":
    # Get configuration from environment or use defaults
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", 8000))
    
    print(f"""
    ╔════════════════════════════════════════╗
    ║   DVD Collection Tracker API           ║
    ╠════════════════════════════════════════╣
    ║   Starting server...                   ║
    ║   API: http://{host}:{port}         ║
    ║   Docs: http://{host}:{port}/docs   ║
    ╚════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        reload=True,  # Auto-reload on code changes
        log_level="info"
    )