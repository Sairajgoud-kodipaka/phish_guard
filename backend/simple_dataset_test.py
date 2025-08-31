#!/usr/bin/env python3
"""
Simple Dataset Test Script
Tests just the dataset download functionality
"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to Python path
current_dir = Path(__file__).parent
app_dir = current_dir / "app"
sys.path.insert(0, str(current_dir))

from app.services.dataset_manager import dataset_manager

async def simple_test():
    """Simple test of dataset download"""
    print("🧪 Simple Dataset Test...")
    print("=" * 40)
    
    try:
        # Test dataset download
        print("📥 Downloading spam dataset...")
        path = await dataset_manager.download_spam_dataset()
        
        if path:
            print(f"✅ Dataset downloaded to: {path}")
            
            # List contents of the dataset directory
            dataset_path = Path(path)
            if dataset_path.exists():
                print(f"📁 Dataset directory contents:")
                for item in dataset_path.iterdir():
                    if item.is_file():
                        print(f"   📄 {item.name} ({item.stat().st_size} bytes)")
                    else:
                        print(f"   📁 {item.name}/")
            
            return True
        else:
            print("❌ Dataset download failed")
            return False
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🚀 PhishGuard Simple Dataset Test")
    print("=" * 40)
    
    success = await simple_test()
    
    if success:
        print("\n✅ Dataset download test completed successfully!")
        print("🎯 You can now proceed to the full ML integration test!")
    else:
        print("\n❌ Dataset download test failed!")
        print("🔧 Please check the error messages above")
    
    print("\n" + "=" * 40)

if __name__ == "__main__":
    asyncio.run(main())
