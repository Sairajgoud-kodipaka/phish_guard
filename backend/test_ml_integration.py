#!/usr/bin/env python3
"""
Test ML Integration Script
Tests the complete ML pipeline: dataset download, model training, and email analysis
"""

import asyncio
import sys
from pathlib import Path

# Add the app directory to Python path
current_dir = Path(__file__).parent
app_dir = current_dir / "app"
sys.path.insert(0, str(current_dir))

from app.services.dataset_manager import dataset_manager
from app.services.enhanced_threat_analyzer import enhanced_analyzer

async def test_complete_ml_pipeline():
    """Test the complete ML pipeline"""
    print("🧪 Testing Complete ML Integration Pipeline...")
    print("=" * 60)
    
    try:
        # Step 1: Download and load dataset
        print("📥 Step 1: Downloading spam dataset...")
        path = await dataset_manager.download_spam_dataset()
        
        if not path:
            print("❌ Dataset download failed")
            return False
        
        print(f"✅ Dataset downloaded to: {path}")
        
        # Step 2: Load dataset into DataFrame
        print("\n📊 Step 2: Loading dataset...")
        df = await dataset_manager.load_spam_dataset()
        
        if df is None:
            print("❌ Dataset loading failed")
            return False
        
        print(f"✅ Dataset loaded: {len(df)} rows, {len(df.columns)} columns")
        print(f"📋 Columns: {list(df.columns)}")
        
        # Step 3: Train ML model
        print("\n🤖 Step 3: Training ML model...")
        
        # Find the CSV file in the dataset directory
        csv_files = list(Path(path).glob("*.csv"))
        if not csv_files:
            print("❌ No CSV files found in dataset directory")
            return False
        
        csv_path = str(csv_files[0])
        print(f"📁 Using dataset file: {csv_path}")
        
        # Train the model
        training_success = await enhanced_analyzer.train_model(csv_path)
        
        if not training_success:
            print("❌ Model training failed")
            return False
        
        print("✅ Model trained successfully!")
        
        # Step 4: Test email analysis
        print("\n🔍 Step 4: Testing email analysis...")
        
        # Test with a spam email
        spam_email = """
        URGENT! LIMITED TIME OFFER!
        You've been selected for a special discount!
        Click here to claim your prize: http://suspicious-link.com
        Don't miss out on this amazing opportunity!
        """
        
        print("📧 Testing spam email detection...")
        spam_result = await enhanced_analyzer.analyze_email(spam_email)
        print(f"   Result: {spam_result['threat_level']} threat")
        print(f"   Confidence: {spam_result['confidence']:.3f}")
        print(f"   Is Spam: {spam_result['is_spam']}")
        
        # Test with a legitimate email
        legitimate_email = """
        Hi John,
        
        Thank you for your recent order. Your package has been shipped
        and will arrive within 3-5 business days.
        
        Best regards,
        Customer Service Team
        """
        
        print("\n📧 Testing legitimate email detection...")
        legit_result = await enhanced_analyzer.analyze_email(legitimate_email)
        print(f"   Result: {legitimate_result['threat_level']} threat")
        print(f"   Confidence: {legitimate_result['confidence']:.3f}")
        print(f"   Is Spam: {legitimate_result['is_spam']}")
        
        # Step 5: Get model information
        print("\n📋 Step 5: Model information...")
        model_info = await enhanced_analyzer.get_model_info()
        print(f"   Model trained: {model_info['is_trained']}")
        print(f"   Model directory: {model_info['model_directory']}")
        print(f"   Model file exists: {model_info['model_file_exists']}")
        print(f"   Model type: {model_info['model_type']}")
        
        # Step 6: Save dataset info
        print("\n💾 Step 6: Saving dataset information...")
        await dataset_manager.save_dataset_info()
        print("✅ Dataset information saved")
        
        print("\n🎉 All ML integration tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_email_analysis():
    """Test email analysis with various examples"""
    print("\n📧 Testing Email Analysis with Various Examples...")
    print("=" * 50)
    
    test_emails = [
        {
            "name": "Obvious Spam",
            "content": "FREE VIAGRA NOW! CLICK HERE! LIMITED TIME OFFER!",
            "expected": "spam"
        },
        {
            "name": "Suspicious Phishing",
            "content": "Your account has been suspended. Click here to verify: http://fake-bank.com",
            "expected": "spam"
        },
        {
            "name": "Legitimate Business",
            "content": "Dear customer, your order #12345 has been confirmed and will ship tomorrow.",
            "expected": "ham"
        },
        {
            "name": "Personal Email",
            "content": "Hi Mom, I'll be home for dinner tonight. Love you!",
            "expected": "ham"
        }
    ]
    
    for test_email in test_emails:
        print(f"\n📧 Testing: {test_email['name']}")
        result = await enhanced_analyzer.analyze_email(test_email['content'])
        
        print(f"   Content: {test_email['content'][:50]}...")
        print(f"   Prediction: {'Spam' if result['is_spam'] else 'Ham'}")
        print(f"   Threat Level: {result['threat_level']}")
        print(f"   Confidence: {result['confidence']:.3f}")
        
        # Check if prediction matches expectation
        prediction = "spam" if result['is_spam'] else "ham"
        if prediction == test_email['expected']:
            print("   ✅ Prediction matches expectation")
        else:
            print("   ❌ Prediction doesn't match expectation")

async def main():
    """Main test function"""
    print("🚀 PhishGuard ML Integration Test Suite")
    print("=" * 60)
    
    # Test the complete pipeline
    success = await test_complete_ml_pipeline()
    
    if success:
        print("\n✅ ML integration test completed successfully!")
        
        # Test email analysis with various examples
        await test_email_analysis()
        
        print("\n🎯 Your PhishGuard ML system is ready for production!")
        print("🔍 You can now analyze emails for spam and threats!")
        
    else:
        print("\n❌ ML integration test failed!")
        print("🔧 Please check the error messages above")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
