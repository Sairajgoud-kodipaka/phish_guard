"""
Dashboard Schemas
Pydantic models for dashboard data
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, date


class DashboardStats(BaseModel):
    """Dashboard statistics schema"""
    total_emails: int = Field(..., description="Total emails processed")
    emails_processed: int = Field(..., description="Emails processed in period")
    threats_detected: int = Field(..., description="Threats detected in period")
    blocked_emails: int = Field(..., description="Emails blocked in period")
    quarantined_emails: int = Field(..., description="Emails quarantined in period")
    accuracy_percentage: float = Field(..., description="Detection accuracy percentage")
    false_positives: int = Field(..., description="False positives in period")
    period_days: int = Field(..., description="Period in days")


class ThreatTimelineItem(BaseModel):
    """Threat timeline item schema"""
    timeline_date: date = Field(..., description="Date")
    threat_level: str = Field(..., description="Threat level")
    count: int = Field(..., description="Number of threats")


class EmailActivityItem(BaseModel):
    """Email activity item schema"""
    timestamp: datetime = Field(..., description="Activity timestamp")
    email_count: int = Field(..., description="Number of emails")
    threat_count: int = Field(..., description="Number of threats")


class ThreatDistribution(BaseModel):
    """Threat distribution schema"""
    threat_type: str = Field(..., description="Type of threat")
    count: int = Field(..., description="Number of occurrences")
    percentage: float = Field(..., description="Percentage of total")
    avg_risk_score: float = Field(..., description="Average risk score")


class RecentActivity(BaseModel):
    """Recent activity schema"""
    type: str = Field(..., description="Activity type")
    description: str = Field(..., description="Activity description")
    severity: str = Field(..., description="Activity severity")
    timestamp: datetime = Field(..., description="Activity timestamp")
    details: Dict[str, Any] = Field(..., description="Additional details")


class SystemMetrics(BaseModel):
    """System metrics schema"""
    cpu_usage: float = Field(..., description="CPU usage percentage")
    memory_usage: float = Field(..., description="Memory usage percentage")
    disk_usage: float = Field(..., description="Disk usage percentage")
    active_connections: int = Field(..., description="Active database connections")
    emails_per_minute: float = Field(..., description="Emails processed per minute")


class PerformanceMetrics(BaseModel):
    """Performance metrics schema"""
    avg_processing_time: float = Field(..., description="Average processing time in seconds")
    peak_processing_time: float = Field(..., description="Peak processing time in seconds")
    emails_pending: int = Field(..., description="Emails pending processing")
    queue_depth: int = Field(..., description="Processing queue depth")
    throughput: float = Field(..., description="Emails per second throughput") 