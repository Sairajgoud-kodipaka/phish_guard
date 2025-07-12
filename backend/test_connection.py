#!/usr/bin/env python3
"""
PhishGuard Backend Connection Test
Verify all frontend endpoints are working correctly
"""

import asyncio
import httpx
import json
from datetime import datetime

async def test_backend_connection():
    """Test all endpoints that the frontend expects"""
    
    base_url = "http://localhost:8001"
    
    test_results = {
        "passed": 0,
        "failed": 0,
        "tests": []
    }
    
    # Test endpoints
    endpoints = [
        ("GET", "/health", "Health check"),
        ("GET", "/api/v1/emails/stats/summary?days=30", "Email statistics"),
        ("GET", "/api/v1/emails/?limit=10&days=30", "Recent emails"),  # Added trailing slash
        ("GET", "/api/v1/dashboard/stats?days=30", "Dashboard stats"),
        ("GET", "/api/v1/dashboard/recent-activity?limit=10", "Recent activity"),
        ("GET", "/api/v1/dashboard/threat-timeline?days=7", "Threat timeline"),
        ("GET", "/api/v1/dashboard/threat-distribution?days=30", "Threat distribution"),
    ]
    
    # Keep client open for all tests
    async with httpx.AsyncClient(timeout=30.0) as client:
        # Test regular endpoints
        for method, endpoint, description in endpoints:
            try:
                print(f"Testing {description}...")
                response = await client.request(method, f"{base_url}{endpoint}")
                
                if response.status_code == 200:
                    test_results["passed"] += 1
                    test_results["tests"].append({
                        "endpoint": endpoint,
                        "description": description,
                        "status": "PASS",
                        "response_size": len(response.content)
                    })
                    print(f"  ✅ {description} - OK")
                else:
                    test_results["failed"] += 1
                    test_results["tests"].append({
                        "endpoint": endpoint,
                        "description": description,
                        "status": "FAIL",
                        "error": f"HTTP {response.status_code}"
                    })
                    print(f"  ❌ {description} - HTTP {response.status_code}")
                    if response.status_code in [307, 308]:
                        print(f"     Redirect Location: {response.headers.get('location', 'Not specified')}")
                        
            except Exception as e:
                test_results["failed"] += 1
                test_results["tests"].append({
                    "endpoint": endpoint,
                    "description": description,
                    "status": "FAIL",
                    "error": str(e)
                })
                print(f"  ❌ {description} - {str(e)}")
        
        # Test sample email analysis (within same client context)
        try:
            print("\nTesting email analysis...")
            sample_email = """From: urgent-payment@fake-bank.com
To: user@example.com
Subject: URGENT: Verify Your Account Now!

Dear Customer,

Your account has been suspended due to suspicious activity. 
Click here to verify your account immediately: http://fake-bank.com/verify

This is urgent and must be completed within 24 hours.

Thank you,
Security Team"""
            
            response = await client.post(
                f"{base_url}/api/v1/emails/analyze-text",
                json={"content": sample_email}
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"  ✅ Email analysis - Threat Score: {result.get('threat_score', 0):.2f}")
                print(f"     Threat Level: {result.get('threat_level', 'unknown')}")
                print(f"     Recommended Action: {result.get('recommended_action', 'unknown')}")
                print(f"     Indicators: {', '.join(result.get('threat_indicators', [])[:3])}")
                test_results["passed"] += 1
            else:
                print(f"  ❌ Email analysis - HTTP {response.status_code}")
                print(f"     Response: {response.text[:200]}")
                test_results["failed"] += 1
                
        except Exception as e:
            print(f"  ❌ Email analysis - {str(e)}")
            test_results["failed"] += 1
    
    # Summary
    print(f"\n📊 Test Results:")
    print(f"   Passed: {test_results['passed']}")
    print(f"   Failed: {test_results['failed']}")
    print(f"   Total:  {test_results['passed'] + test_results['failed']}")
    
    if test_results["failed"] == 0:
        print("\n🎉 All tests passed! Backend is ready for frontend connection.")
    else:
        print(f"\n⚠️  {test_results['failed']} tests failed. Backend may need to be started or fixed.")
        
        # Show failed tests
        failed_tests = [t for t in test_results["tests"] if t["status"] == "FAIL"]
        if failed_tests:
            print("\n❌ Failed Tests:")
            for test in failed_tests:
                print(f"   - {test['description']}: {test.get('error', 'Unknown error')}")
    
    return test_results

if __name__ == "__main__":
    print("🔍 Testing PhishGuard Backend Connection...")
    print("=" * 50)
    
    try:
        results = asyncio.run(test_backend_connection())
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}") 