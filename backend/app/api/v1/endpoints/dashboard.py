"""
Dashboard API Endpoints
Real-time statistics and overview data
"""

from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_, desc

from app.core.database import get_async_db
from app.models.email import Email
from app.models.threat import Threat
from app.schemas.dashboard import (
    DashboardStats,
    ThreatTimelineItem,
    EmailActivityItem,
    ThreatDistribution,
    RecentActivity
)

router = APIRouter()


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_async_db),
    days: int = Query(default=30, description="Number of days for statistics")
):
    """Get dashboard statistics from real database"""
    try:
        organization_id = 1  # Demo organization ID
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total emails
        total_query = select(func.count(Email.id)).where(
            and_(
                Email.organization_id == organization_id,
                Email.date_received >= start_date
            )
        )
        total_result = await db.execute(total_query)
        total_emails = total_result.scalar() or 0
        
        # Threat level counts
        threat_query = select(
            Email.threat_level,
            func.count(Email.id).label("count")
        ).where(
            and_(
                Email.organization_id == organization_id,
                Email.date_received >= start_date
            )
        ).group_by(Email.threat_level)
        
        threat_result = await db.execute(threat_query)
        threat_counts = {row.threat_level: row.count for row in threat_result}
        
        # Calculate stats
        threats_detected = (
            threat_counts.get('high', 0) + 
            threat_counts.get('critical', 0) + 
            threat_counts.get('medium', 0)
        )
        
        # Quarantined emails
        quarantine_query = select(func.count(Email.id)).where(
            and_(
                Email.organization_id == organization_id,
                Email.date_received >= start_date,
                Email.quarantined == True
            )
        )
        quarantine_result = await db.execute(quarantine_query)
        quarantined_emails = quarantine_result.scalar() or 0
        
        # Blocked emails (same as quarantined for now)
        blocked_emails = quarantined_emails
        
        # False positives (would need separate tracking)
        false_positives = 0
        
        # Accuracy calculation
        clean_emails = threat_counts.get('clean', 0) + threat_counts.get('low', 0)
        accuracy_percentage = ((clean_emails + threats_detected) / max(total_emails, 1)) * 100
        
        return DashboardStats(
            total_emails=total_emails,
            emails_processed=total_emails,
            threats_detected=threats_detected,
            blocked_emails=blocked_emails,
            quarantined_emails=quarantined_emails,
            accuracy_percentage=round(accuracy_percentage, 1),
            false_positives=false_positives,
            period_days=days
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch dashboard statistics: {str(e)}"
        )


@router.get("/threat-timeline", response_model=List[ThreatTimelineItem])
async def get_threat_timeline(
    db: AsyncSession = Depends(get_async_db),
    days: int = Query(default=7, description="Number of days for timeline")
):
    """Get threat detection timeline from real data"""
    try:
        organization_id = 1  # Demo organization ID
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Group emails by date and threat level
        stmt = select(
            func.date(Email.date_received).label("date"),
            Email.threat_level,
            func.count(Email.id).label("count")
        ).where(
            and_(
                Email.organization_id == organization_id,
                Email.date_received >= start_date
            )
        ).group_by(
            func.date(Email.date_received),
            Email.threat_level
        ).order_by(
            func.date(Email.date_received)
        )
        
        result = await db.execute(stmt)
        timeline_data = result.fetchall()
        
        # Process results into timeline format
        timeline_items = []
        for row in timeline_data:
            timeline_items.append(ThreatTimelineItem(
                timeline_date=row.date,
                threat_level=row.threat_level,
                count=row.count
            ))
        
        return timeline_items
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch threat timeline: {str(e)}"
        )


@router.get("/email-activity", response_model=List[EmailActivityItem])
async def get_email_activity(
    db: AsyncSession = Depends(get_async_db),
    hours: int = Query(default=24, description="Number of hours for activity")
):
    """Get recent email activity from real data"""
    try:
        organization_id = 1  # Demo organization ID
        start_time = datetime.utcnow() - timedelta(hours=hours)
        
        # Get hourly email activity (simplified for SQLite)
        stmt = select(
            func.strftime('%Y-%m-%d %H:00:00', Email.date_received).label("hour"),
            func.count(Email.id).label("email_count"),
            func.sum(
                func.case(
                    (Email.threat_level.in_(['medium', 'high', 'critical']), 1),
                    else_=0
                )
            ).label("threat_count")
        ).where(
            and_(
                Email.organization_id == organization_id,
                Email.date_received >= start_time
            )
        ).group_by(
            func.strftime('%Y-%m-%d %H:00:00', Email.date_received)
        ).order_by(
            func.strftime('%Y-%m-%d %H:00:00', Email.date_received)
        )
        
        result = await db.execute(stmt)
        activity_data = result.fetchall()
        
        # Process results
        activity_items = []
        for row in activity_data:
            # Parse the hour string back to datetime
            hour_dt = datetime.strptime(row.hour, '%Y-%m-%d %H:%M:%S')
            activity_items.append(EmailActivityItem(
                timestamp=hour_dt,
                email_count=row.email_count,
                threat_count=row.threat_count or 0
            ))
        
        return activity_items
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch email activity: {str(e)}"
        )


@router.get("/threat-distribution", response_model=List[ThreatDistribution])
async def get_threat_distribution(
    db: AsyncSession = Depends(get_async_db),
    days: int = Query(default=30, description="Number of days for distribution")
):
    """Get threat type distribution from real data"""
    try:
        organization_id = 1  # Demo organization ID
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Get threat distribution by type from threats table
        stmt = select(
            Threat.threat_type,
            func.count(Threat.id).label("count"),
            func.avg(Threat.risk_score).label("avg_risk_score")
        ).join(
            Email, Email.id == Threat.email_id
        ).where(
            and_(
                Email.organization_id == organization_id,
                Email.date_received >= start_date
            )
        ).group_by(
            Threat.threat_type
        ).order_by(
            func.count(Threat.id).desc()
        )
        
        result = await db.execute(stmt)
        distribution_data = result.fetchall()
        
        # Also get total count for percentage calculation
        total_threats = sum(row.count for row in distribution_data)
        
        # Process results
        distribution_items = []
        for row in distribution_data:
            percentage = (row.count / max(total_threats, 1)) * 100
            distribution_items.append(ThreatDistribution(
                threat_type=row.threat_type,
                count=row.count,
                percentage=round(percentage, 1),
                avg_risk_score=round(row.avg_risk_score or 0, 2)
            ))
        
        return distribution_items
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch threat distribution: {str(e)}"
        )


@router.get("/recent-activity", response_model=List[RecentActivity])
async def get_recent_activity(
    db: AsyncSession = Depends(get_async_db),
    limit: int = Query(default=10, description="Number of recent activities")
):
    """Get recent security activities from real email data"""
    try:
        organization_id = 1  # Demo organization ID
        
        # Get recent emails with threats
        stmt = select(Email).where(
            and_(
                Email.organization_id == organization_id,
                Email.threat_level.in_(['medium', 'high', 'critical'])
            )
        ).order_by(desc(Email.date_received)).limit(limit)
        
        result = await db.execute(stmt)
        recent_emails = result.scalars().all()
        
        # Convert to activity format
        activities = []
        for email in recent_emails:
            # Determine activity type and description
            if email.threat_level == 'critical':
                activity_type = "threat_blocked"
                description = f"Critical threat blocked: {email.subject[:50]}... from {email.sender_email}"
                severity = "critical"
            elif email.threat_level == 'high':
                activity_type = "threat_detected"
                description = f"High-risk email quarantined: {email.subject[:50]}... from {email.sender_email}"
                severity = "high"
            else:
                activity_type = "threat_flagged"
                description = f"Suspicious email flagged: {email.subject[:50]}... from {email.sender_email}"
                severity = "medium"
            
            activities.append(RecentActivity(
                type=activity_type,
                description=description,
                severity=severity,
                timestamp=email.date_received.isoformat(),
                details={
                    "email_id": email.id,
                    "threat_score": email.threat_score,
                    "sender": email.sender_email,
                    "action_taken": email.action_taken
                }
            ))
        
        return activities
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch recent activity: {str(e)}"
        )


@router.get("/system-health")
async def get_system_health(
    db: AsyncSession = Depends(get_async_db)
):
    """Get system health status"""
    try:
        # Check database connectivity
        await db.execute(select(1))
        
        # Get processing statistics
        organization_id = 1  # Demo organization ID
        
        # Emails pending processing
        pending_stmt = select(func.count(Email.id)).where(
            and_(
                Email.organization_id == organization_id,
                Email.status == "pending"
            )
        )
        pending_result = await db.execute(pending_stmt)
        pending_count = pending_result.scalar() or 0
        
        # Average processing time
        avg_time_stmt = select(func.avg(Email.processing_time)).where(
            and_(
                Email.organization_id == organization_id,
                Email.processing_time.isnot(None)
            )
        )
        avg_time_result = await db.execute(avg_time_stmt)
        avg_processing_time = avg_time_result.scalar() or 0
        
        return {
            "status": "healthy",
            "database": "connected",
            "pending_emails": pending_count,
            "avg_processing_time": round(avg_processing_time, 2),
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.utcnow().isoformat()
        } 