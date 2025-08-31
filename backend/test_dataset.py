#!/usr/bin/env python3
"""
Test Dataset Integration Script
Tests the dataset download and loading functionality
"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to Python path
current_dir = Path(__file__).parent
app_dir = current_dir / "app"
sys.path.insert(0, str(current_dir))

from app.services.dataset_manager import dataset_manager

async def test_dataset_download():
    """Test the dataset download functionality"""
    print("🧪 Testing Dataset Integration...")
    print("=" * 50)
    
    try:
        # Test dataset download
        print("📥 Testing dataset download...")
        path = await dataset_manager.download_spam_dataset()
        
        if path:
            print(f"✅ Dataset downloaded successfully to: {path}")
        else:
            print("❌ Dataset download failed")
            return False
        
        # Test dataset loading
        print("\n📊 Testing dataset loading...")
        df = await dataset_manager.load_spam_dataset()
        
        if df is not None:
            print(f"✅ Dataset loaded successfully!")
            print(f"   📈 Rows: {len(df)}")
            print(f"   📋 Columns: {list(df.columns)}")
            print(f"   🔍 Sample data:")
            print(df.head())
        else:
            print("❌ Dataset loading failed")
            return False
        
        # Test dataset info
        print("\n📋 Testing dataset info...")
        info = await dataset_manager.get_dataset_info()
        print(f"✅ Dataset info retrieved:")
        print(f"   📁 Data directory: {info['data_directory']}")
        print(f"   📊 Total datasets: {info['total_datasets']}")
        
        # Save dataset info
        print("\n💾 Saving dataset info...")
        await dataset_manager.save_dataset_info()
        print("✅ Dataset info saved")
        
        print("\n🎉 All tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🚀 PhishGuard Dataset Integration Test")
    print("=" * 50)
    
    success = await test_dataset_download()
    
    if success:
        print("\n✅ Dataset integration test completed successfully!")
        print("🎯 You can now use the dataset for training and testing!")
    else:
        print("\n❌ Dataset integration test failed!")
        print("🔧 Please check the error messages above")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    asyncio.run(main())
