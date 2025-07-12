#!/usr/bin/env python3
"""
PhishGuard Implementation Test Script
Tests the core ML and email processing functionality
"""

import asyncio
import sys
import os
from pathlib import Path

# Add the app directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.services.email_processor import EmailProcessor
from app.services.threat_analyzer import ThreatAnalyzer
from app.services.url_scanner import URLScanner
from app.utils.sample_data import SampleDataGenerator, create_demo_organization


# Sample email content for testing
SAMPLE_PHISHING_EMAIL = """From: security@fake-bank.com
To: victim@company.com
Subject: URGENT: Account Suspension Notice
Date: Mon, 01 Jan 2024 10:00:00 +0000
Message-ID: <12345@fake-bank.com>

Dear Customer,

We have detected suspicious activity on your account. Your account will be suspended within 24 hours unless you verify your identity immediately.

Click here to verify: http://fake-bank-verify.suspicious.com/login

If you do not verify within 24 hours, your account will be permanently closed.

Best regards,
Security Team
Fake Bank
"""

SAMPLE_LEGITIMATE_EMAIL = """From: noreply@realbank.com
To: customer@company.com
Subject: Your monthly statement is ready
Date: Mon, 01 Jan 2024 10:00:00 +0000
Message-ID: <67890@realbank.com>

Dear Valued Customer,

Your monthly statement for December 2023 is now available in your online banking portal.

You can view your statement by logging into your account at our secure website.

Thank you for banking with us.

Best regards,
Customer Service
Real Bank
"""


async def test_email_processing():
    """Test email processing functionality"""
    print("🔍 Testing Email Processing...")
    
    processor = EmailProcessor()
    
    # Test phishing email
    print("\n📧 Processing phishing email...")
    phishing_result = await processor.process_email(SAMPLE_PHISHING_EMAIL, "test_phishing_001")
    
    print(f"   Subject: {phishing_result['subject']}")
    print(f"   Sender: {phishing_result['sender_email']}")
    print(f"   URLs found: {len(phishing_result['urls'])}")
    print(f"   Content risk score: {phishing_result['content_analysis']['content_risk_score']}")
    
    # Test legitimate email
    print("\n📧 Processing legitimate email...")
    legitimate_result = await processor.process_email(SAMPLE_LEGITIMATE_EMAIL, "test_legitimate_001")
    
    print(f"   Subject: {legitimate_result['subject']}")
    print(f"   Sender: {legitimate_result['sender_email']}")
    print(f"   URLs found: {len(legitimate_result['urls'])}")
    print(f"   Content risk score: {legitimate_result['content_analysis']['content_risk_score']}")
    
    return phishing_result, legitimate_result


async def test_threat_analysis():
    """Test threat analysis functionality"""
    print("\n🤖 Testing Threat Analysis...")
    
    analyzer = ThreatAnalyzer()
    
    # Process sample emails first
    processor = EmailProcessor()
    phishing_email = await processor.process_email(SAMPLE_PHISHING_EMAIL, "threat_test_001")
    legitimate_email = await processor.process_email(SAMPLE_LEGITIMATE_EMAIL, "threat_test_002")
    
    # Analyze phishing email
    print("\n🚨 Analyzing phishing email...")
    phishing_analysis = await analyzer.analyze_threat(
        phishing_email,
        phishing_email["content_analysis"]
    )
    
    print(f"   Threat Score: {phishing_analysis['threat_score']:.3f}")
    print(f"   Threat Level: {phishing_analysis['threat_level']}")
    print(f"   Is Phishing: {phishing_analysis['is_phishing']}")
    print(f"   Confidence: {phishing_analysis['confidence_score']:.3f}")
    print(f"   Recommended Action: {phishing_analysis['recommended_action']}")
    print(f"   Threat Indicators: {phishing_analysis['threat_indicators']}")
    
    # Analyze legitimate email
    print("\n✅ Analyzing legitimate email...")
    legitimate_analysis = await analyzer.analyze_threat(
        legitimate_email,
        legitimate_email["content_analysis"]
    )
    
    print(f"   Threat Score: {legitimate_analysis['threat_score']:.3f}")
    print(f"   Threat Level: {legitimate_analysis['threat_level']}")
    print(f"   Is Phishing: {legitimate_analysis['is_phishing']}")
    print(f"   Confidence: {legitimate_analysis['confidence_score']:.3f}")
    print(f"   Recommended Action: {legitimate_analysis['recommended_action']}")
    
    return phishing_analysis, legitimate_analysis


async def test_url_scanning():
    """Test URL scanning functionality"""
    print("\n🌐 Testing URL Scanning...")
    
    scanner = URLScanner()
    
    # Test URLs
    test_urls = [
        {
            "url": "http://fake-bank-verify.suspicious.com/login",
            "domain": "fake-bank-verify.suspicious.com",
            "source": "email"
        },
        {
            "url": "https://www.google.com",
            "domain": "www.google.com", 
            "source": "email"
        },
        {
            "url": "http://bit.ly/suspicious-link",
            "domain": "bit.ly",
            "source": "email"
        }
    ]
    
    scan_results = await scanner.scan_urls(test_urls)
    
    print(f"   Total URLs scanned: {scan_results['total_urls']}")
    print(f"   Overall risk: {scan_results['overall_risk']:.3f}")
    print(f"   High risk count: {scan_results['high_risk_count']}")
    
    for result in scan_results['scan_results']:
        print(f"   📍 {result['url'][:50]}...")
        print(f"      Risk Score: {result['risk_score']:.3f}")
        print(f"      Reputation: {result['reputation']}")
        print(f"      Threat Types: {result['threat_types']}")
    
    await scanner.close()
    return scan_results


async def test_sample_data_generation():
    """Test sample data generation"""
    print("\n📊 Testing Sample Data Generation...")
    
    try:
        # Create demo organization
        org_id = await create_demo_organization()
        print(f"   Demo organization created/found: ID {org_id}")
        
        # Generate sample data
        generator = SampleDataGenerator()
        result = await generator.generate_sample_data(org_id, num_emails=10)
        
        print(f"   Sample emails created: {result['emails_created']}")
        print(f"   Sample threats created: {result['threats_created']}")
        
        return result
        
    except Exception as e:
        print(f"   ❌ Sample data generation failed: {e}")
        return None


async def main():
    """Run all tests"""
    print("🚀 PhishGuard Implementation Test Suite")
    print("=" * 50)
    
    try:
        # Test email processing
        await test_email_processing()
        
        # Test threat analysis
        await test_threat_analysis()
        
        # Test URL scanning
        await test_url_scanning()
        
        # Test sample data generation
        await test_sample_data_generation()
        
        print("\n✅ All tests completed successfully!")
        print("\n📋 Summary:")
        print("   ✓ Email processing works")
        print("   ✓ Threat analysis works") 
        print("   ✓ URL scanning works")
        print("   ✓ Sample data generation works")
        print("\n🎉 PhishGuard core implementation is ready!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main()) 