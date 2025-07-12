#!/usr/bin/env python3
"""
PhishGuard Demo Backend Server
Simple startup script for demo purposes
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the app directory to Python path
current_dir = Path(__file__).parent
app_dir = current_dir / "app"
sys.path.insert(0, str(current_dir))

def main():
    """Run the demo backend server"""
    print("🚀 Starting PhishGuard Demo Backend...")
    print("📊 Dashboard will be available at: http://localhost:3000")
    print("📖 API Documentation: http://localhost:8001/docs")
    print("❤️  Health Check: http://localhost:8001/health")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    # Set demo environment variables
    os.environ.setdefault("ENVIRONMENT", "development")
    os.environ.setdefault("DEBUG", "true")
    
    try:
        uvicorn.run(
            "app.main:app",
            host="0.0.0.0",
            port=8001,
            reload=True,
            log_level="info",
            access_log=False  # Reduce noise
        )
    except KeyboardInterrupt:
        print("\n🛑 Demo backend stopped.")
    except Exception as e:
        print(f"❌ Error starting backend: {e}")
        print("💡 Make sure you're in the backend directory and have installed dependencies")

if __name__ == "__main__":
    main() 