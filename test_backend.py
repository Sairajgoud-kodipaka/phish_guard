#!/usr/bin/env python3
"""
Simple test script to check if the backend can start
"""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    print("Testing backend imports...")
    
    # Test basic imports
    from app.core.config import settings
    print("✅ Config imported successfully")
    
    from app.core.database import engine, Base
    print("✅ Database imported successfully")
    
    from app.models.email import Email
    print("✅ Email model imported successfully")
    
    from app.api.v1.endpoints.emails import router
    print("✅ Emails router imported successfully")
    
    from app.main import app
    print("✅ Main app imported successfully")
    
    print("\n🎉 All imports successful! Backend should work.")
    
except Exception as e:
    print(f"❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
