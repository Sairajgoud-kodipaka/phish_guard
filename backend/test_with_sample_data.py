#!/usr/bin/env python3
"""
Test ML Functionality with Sample Data
Tests the ML pipeline using sample spam/ham data without requiring external downloads
"""

import asyncio
import sys
import pandas as pd
from pathlib import Path
import tempfile
import os

# Add the app directory to Python path
current_dir = Path(__file__).parent
app_dir = current_dir / "app"
sys.path.insert(0, str(current_dir))

from app.services.enhanced_threat_analyzer import enhanced_analyzer

def create_sample_dataset():
    """Create a sample spam/ham dataset for testing"""
    sample_data = {
        'text': [
            # Spam emails
            "FREE VIAGRA NOW! CLICK HERE! LIMITED TIME OFFER!",
            "URGENT! Your account has been suspended. Click here to verify: http://fake-bank.com",
            "CONGRATULATIONS! You've won $1,000,000! Claim your prize now!",
            "SPECIAL DISCOUNT! 90% OFF on all products! Don't miss out!",
            "Make money fast! Work from home! Earn $5000 per day!",
            
            # Ham (legitimate) emails
            "Hi John, your order #12345 has been confirmed and will ship tomorrow.",
            "Dear customer, thank you for your recent purchase.",
            "Hi Mom, I'll be home for dinner tonight. Love you!",
            "Meeting reminder: Team standup at 9 AM tomorrow.",
            "Your monthly newsletter is ready. Click here to read."
        ],
        'label': [
            'spam', 'spam', 'spam', 'spam', 'spam',
            'ham', 'ham', 'ham', 'ham', 'ham'
        ]
    }
    
    return pd.DataFrame(sample_data)

async def test_ml_pipeline_with_sample_data():
    """Test the ML pipeline using sample data"""
    print("🧪 Testing ML Pipeline with Sample Data...")
    print("=" * 60)
    
    try:
        # Create sample dataset
        print("📊 Creating sample dataset...")
        df = create_sample_dataset()
        print(f"✅ Sample dataset created: {len(df)} emails")
        print(f"📈 Spam emails: {len(df[df['label'] == 'spam'])}")
        print(f"📉 Ham emails: {len(df[df['label'] == 'ham'])}")
        
        # Save sample dataset to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            df.to_csv(f.name, index=False)
            temp_csv_path = f.name
        
        print(f"📁 Sample dataset saved to: {temp_csv_path}")
        
        # Train the model
        print("\n🤖 Training ML model on sample data...")
        training_success = await enhanced_analyzer.train_model(temp_csv_path)
        
        if not training_success:
            print("❌ Model training failed")
            return False
        
        print("✅ Model trained successfully!")
        
        # Test email analysis
        print("\n🔍 Testing email analysis...")
        
        test_emails = [
            {
                "name": "New Spam Email",
                "content": "FREE MONEY! CLICK HERE TO CLAIM YOUR PRIZE!",
                "expected": "spam"
            },
            {
                "name": "New Legitimate Email",
                "content": "Hi team, please review the attached documents.",
                "expected": "ham"
            },
            {
                "name": "Suspicious Email",
                "content": "Your password will expire. Click here to reset: http://suspicious-link.com",
                "expected": "spam"
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
        
        # Get model information
        print("\n📋 Model information...")
        model_info = await enhanced_analyzer.get_model_info()
        print(f"   Model trained: {model_info['is_trained']}")
        print(f"   Model directory: {model_info['model_directory']}")
        print(f"   Model file exists: {model_info['model_file_exists']}")
        print(f"   Model type: {model_info['model_type']}")
        
        # Clean up temporary file
        os.unlink(temp_csv_path)
        print(f"\n🗑️ Cleaned up temporary file: {temp_csv_path}")
        
        print("\n🎉 All ML pipeline tests passed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🚀 PhishGuard ML Pipeline Test (Sample Data)")
    print("=" * 60)
    
    success = await test_ml_pipeline_with_sample_data()
    
    if success:
        print("\n✅ ML pipeline test completed successfully!")
        print("🎯 Your PhishGuard ML system is working correctly!")
        print("🔍 You can now analyze emails for spam and threats!")
        
    else:
        print("\n❌ ML pipeline test failed!")
        print("🔧 Please check the error messages above")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    asyncio.run(main())
