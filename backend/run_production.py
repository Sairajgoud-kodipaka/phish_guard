#!/usr/bin/env python3
"""
Production PhishGuard Backend Server
Full ML-powered email security analysis system
"""

import os
import sys
import uvicorn
from pathlib import Path

def main():
    """Start the production backend server"""
    
    # Set environment variables for production
    os.environ["PYTHONPATH"] = str(Path(__file__).parent)
    os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./phishguard.db"
    
    print("🚀 Starting PhishGuard Production Backend...")
    print("📊 Full ML capabilities enabled")
    print("🔒 Advanced threat analysis active")
    print("🌐 Server will be available at: http://localhost:8001")
    print("📚 API docs available at: http://localhost:8001/docs")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8001,
            reload=True,
            access_log=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n⛔ Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 