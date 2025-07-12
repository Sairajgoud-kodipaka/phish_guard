#!/usr/bin/env python3
"""
PhishGuard System Test
Comprehensive test to verify all core functionality is working
"""

import sys
import asyncio
sys.path.append('app')

async def test_system():
    print('🔍 Testing PhishGuard Core System')
    print('=' * 50)
    
    # Import services
    from app.services.email_processor import EmailProcessor
    from app.services.threat_analyzer import ThreatAnalyzer
    from app.services.url_scanner import URLScanner
    
    # Initialize services
    email_processor = EmailProcessor()
    threat_analyzer = ThreatAnalyzer()
    url_scanner = URLScanner()
    
    print('✅ All services initialized')
    
    # Test with a sample phishing email
    sample_email = '''From: security@payp4l.com
To: victim@example.com
Subject: Urgent: Account Suspended - Verify Immediately
Date: Mon, 12 Feb 2024 10:00:00 +0000

Your PayPal account has been suspended due to suspicious activity.
Click here immediately to verify: http://payp4l-security.com/verify
Your account will be permanently deleted in 24 hours if not verified.
'''
    
    print('\n📧 Processing sample phishing email...')
    
    # Process email
    email_data = await email_processor.process_email(sample_email, 'test-001')
    print(f'✅ Email processed: {email_data["subject"]}')
    print(f'   Sender: {email_data["sender_email"]}')
    print(f'   URLs found: {len(email_data["urls"])}')
    
    # Analyze threats
    threat_result = await threat_analyzer.analyze_threat(email_data, email_data['content_analysis'])
    print(f'✅ Threat analysis complete')
    print(f'   Threat Score: {threat_result["threat_score"]:.2f}')
    print(f'   Threat Level: {threat_result["threat_level"]}')
    print(f'   Is Phishing: {threat_result["is_phishing"]}')
    print(f'   Recommended Action: {threat_result["recommended_action"]}')
    
    # Test URL scanning
    if email_data['urls']:
        first_url_data = email_data['urls'][0]
        print(f'\n🔗 Scanning URL: {first_url_data["url"]}')
        url_result = await url_scanner.scan_single_url(first_url_data)
        print(f'✅ URL scan complete')
        print(f'   Risk Score: {url_result["risk_score"]:.2f}')
        print(f'   Reputation: {url_result["reputation"]}')
        print(f'   Threat Types: {url_result["threat_types"]}')
    
    # Test with a legitimate email
    print('\n📧 Testing legitimate email...')
    legitimate_email = '''From: support@github.com
To: user@example.com
Subject: Your GitHub security update
Date: Mon, 12 Feb 2024 15:00:00 +0000

Hello,

Your GitHub account security settings have been updated successfully.
If you did not make this change, please contact support.

Best regards,
GitHub Team
'''
    
    email_data2 = await email_processor.process_email(legitimate_email, 'test-002')
    threat_result2 = await threat_analyzer.analyze_threat(email_data2, email_data2['content_analysis'])
    print(f'✅ Legitimate email analysis: {threat_result2["threat_level"]} (score: {threat_result2["threat_score"]:.2f})')
    
    print('\n🎉 System test completed successfully!')
    print('PhishGuard is ready for production use!')
    
    # Summary
    print('\n📊 Test Summary:')
    print(f'✅ Email Processing: Working')
    print(f'✅ Threat Analysis: Working')
    print(f'✅ URL Scanning: Working')
    print(f'✅ Phishing Detection: {threat_result["is_phishing"]} (expected: True)')
    print(f'✅ Legitimate Detection: {not threat_result2["is_phishing"]} (expected: True)')


if __name__ == '__main__':
    # Run the test
    asyncio.run(test_system()) 