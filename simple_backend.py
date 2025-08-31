#!/usr/bin/env python3
"""
Simple FastAPI backend for testing
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta

app = FastAPI(title="Simple PhishGuard Backend")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Simple PhishGuard Backend is running!"}

@app.get("/api/v1/emails")
async def get_emails(limit: int = 10, days: int = 30):
    """Get recent emails - demo data"""
    demo_emails = [
        {
            "id": 1,
            "subject": "Welcome to PhishGuard",
            "sender_email": "noreply@phishguard.com",
            "threat_score": 0.1,
            "threat_level": "clean",
            "is_phishing": False,
            "is_spam": False,
            "is_malware": False,
            "action_taken": "allow",
            "created_at": datetime.utcnow().isoformat(),
            "processing_time": 0.5
        },
        {
            "id": 2,
            "subject": "Security Alert - Suspicious Activity",
            "sender_email": "security@example.com",
            "threat_score": 0.8,
            "threat_level": "high",
            "is_phishing": True,
            "is_spam": False,
            "is_malware": False,
            "action_taken": "quarantine",
            "created_at": (datetime.utcnow() - timedelta(hours=2)).isoformat(),
            "processing_time": 1.2
        }
    ]
    return demo_emails[:limit]

@app.get("/api/v1/emails/stats/summary")
async def get_email_stats(days: int = 30):
    """Get email statistics - demo data"""
    return {
        "period_days": days,
        "total_emails": 2,
        "threat_distribution": {
            "clean": 1,
            "low": 0,
            "medium": 0,
            "high": 1,
            "critical": 0
        },
        "action_distribution": {
            "allow": 1,
            "quarantine": 1,
            "block": 0
        },
        "generated_at": datetime.utcnow().isoformat()
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
