#!/usr/bin/env python3
"""
PhishGuard Backend - Startup Script
Simple script to start the FastAPI server
"""

import uvicorn
import sys
import os

def main():
    """Start the FastAPI server"""
    try:
        print("🚀 Starting PhishGuard Backend...")
        print("📍 Server will run on: http://localhost:8000")
        print("📚 API Documentation: http://localhost:8000/docs")
        print("🔍 Health Check: http://localhost:8000/health")
        print("⏹️  Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Start the server
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
