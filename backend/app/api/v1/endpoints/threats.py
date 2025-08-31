"""
Threat API Endpoints
Threat management and analysis endpoints
"""

from typing import List, Optional
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Query, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc, func
from sqlalchemy.orm import selectinload

from app.core.database import get_async_db
from app.core.security import get_current_user_from_token
from app.models.threat import Threat
from app.models.email import Email
from app.schemas.threat import ThreatResponse, ThreatUpdateRequest, ThreatStatsResponse

router = APIRouter()


@router.get("/", response_model=List[ThreatResponse])
async def get_threats(
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db),
    skip: int = Query(default=0, ge=0, description="Number of records to skip"),
    limit: int = Query(default=50, ge=1, le=100, description="Number of records to return"),
    threat_type: Optional[str] = Query(default=None, description="Filter by threat type"),
    severity: Optional[str] = Query(default=None, description="Filter by severity"),
    status: Optional[str] = Query(default=None, description="Filter by status"),
    resolved: Optional[bool] = Query(default=None, description="Filter by resolution status"),
    days: int = Query(default=30, ge=1, le=365, description="Number of days to look back")
):
    """Get threats for the current user's organization"""
    try:
        organization_id = current_user["organization_id"]
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Build query with join to email for organization filtering
        query = select(Threat).join(Email).where(
            and_(
                Email.organization_id == organization_id,
                Threat.created_at >= start_date
            )
        ).options(selectinload(Threat.email))
        
        # Apply filters
        if threat_type:
            query = query.where(Threat.threat_type == threat_type)
        
        if severity:
            query = query.where(Threat.severity == severity)
        
        if status:
            query = query.where(Threat.status == status)
        
        if resolved is not None:
            query = query.where(Threat.resolved == resolved)
        
        # Add pagination and ordering
        query = query.order_by(desc(Threat.created_at)).offset(skip).limit(limit)
        
        result = await db.execute(query)
        threats = result.scalars().all()
        
        return [ThreatResponse.from_orm(threat) for threat in threats]
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve threats: {str(e)}"
        )


@router.get("/{threat_id}", response_model=ThreatResponse)
async def get_threat(
    threat_id: int,
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db)
):
    """Get a specific threat by ID"""
    try:
        organization_id = current_user["organization_id"]
        
        query = select(Threat).join(Email).where(
            and_(
                Threat.id == threat_id,
                Email.organization_id == organization_id
            )
        ).options(selectinload(Threat.email))
        
        result = await db.execute(query)
        threat = result.scalar_one_or_none()
        
        if not threat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Threat not found"
            )
        
        return ThreatResponse.from_orm(threat)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve threat: {str(e)}"
        )


@router.put("/{threat_id}/investigate")
async def start_investigation(
    threat_id: int,
    notes: str = Form(default="", description="Investigation notes"),
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db)
):
    """Start investigation of a threat"""
    try:
        organization_id = current_user["organization_id"]
        investigator = current_user["email"]
        
        # Get threat
        query = select(Threat).join(Email).where(
            and_(
                Threat.id == threat_id,
                Email.organization_id == organization_id
            )
        )
        result = await db.execute(query)
        threat = result.scalar_one_or_none()
        
        if not threat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Threat not found"
            )
        
        # Start investigation
        threat.start_investigation(investigator)
        if notes:
            threat.investigation_notes = notes
        
        await db.commit()
        
        return {"message": "Investigation started successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start investigation: {str(e)}"
        )


@router.put("/{threat_id}/confirm")
async def confirm_threat(
    threat_id: int,
    notes: str = Form(..., description="Confirmation notes"),
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db)
):
    """Confirm a threat as legitimate"""
    try:
        organization_id = current_user["organization_id"]
        investigator = current_user["email"]
        
        # Get threat
        query = select(Threat).join(Email).where(
            and_(
                Threat.id == threat_id,
                Email.organization_id == organization_id
            )
        )
        result = await db.execute(query)
        threat = result.scalar_one_or_none()
        
        if not threat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Threat not found"
            )
        
        # Confirm threat
        threat.confirm_threat(investigator, notes)
        
        await db.commit()
        
        return {"message": "Threat confirmed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to confirm threat: {str(e)}"
        )


@router.put("/{threat_id}/false-positive")
async def mark_false_positive(
    threat_id: int,
    reason: str = Form(..., description="Reason for marking as false positive"),
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db)
):
    """Mark a threat as false positive"""
    try:
        organization_id = current_user["organization_id"]
        investigator = current_user["email"]
        
        # Get threat
        query = select(Threat).join(Email).where(
            and_(
                Threat.id == threat_id,
                Email.organization_id == organization_id
            )
        )
        result = await db.execute(query)
        threat = result.scalar_one_or_none()
        
        if not threat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Threat not found"
            )
        
        # Mark as false positive
        threat.mark_false_positive(investigator, reason)
        
        await db.commit()
        
        return {"message": "Threat marked as false positive successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to mark as false positive: {str(e)}"
        )


@router.put("/{threat_id}/resolve")
async def resolve_threat(
    threat_id: int,
    resolution_notes: str = Form(..., description="Resolution notes"),
    action_taken: Optional[str] = Form(default=None, description="Action taken to resolve"),
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db)
):
    """Resolve a threat"""
    try:
        organization_id = current_user["organization_id"]
        resolver = current_user["email"]
        
        # Get threat
        query = select(Threat).join(Email).where(
            and_(
                Threat.id == threat_id,
                Email.organization_id == organization_id
            )
        )
        result = await db.execute(query)
        threat = result.scalar_one_or_none()
        
        if not threat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Threat not found"
            )
        
        # Resolve threat
        threat.resolve(resolver, resolution_notes, action_taken)
        
        await db.commit()
        
        return {"message": "Threat resolved successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to resolve threat: {str(e)}"
        )


@router.put("/{threat_id}/escalate")
async def escalate_threat(
    threat_id: int,
    new_severity: str = Form(..., description="New severity level"),
    reason: str = Form(..., description="Reason for escalation"),
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db)
):
    """Escalate threat severity"""
    try:
        organization_id = current_user["organization_id"]
        
        # Validate severity level
        valid_severities = ["low", "medium", "high", "critical"]
        if new_severity not in valid_severities:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid severity level. Must be one of: {valid_severities}"
            )
        
        # Get threat
        query = select(Threat).join(Email).where(
            and_(
                Threat.id == threat_id,
                Email.organization_id == organization_id
            )
        )
        result = await db.execute(query)
        threat = result.scalar_one_or_none()
        
        if not threat:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Threat not found"
            )
        
        # Escalate severity
        threat.escalate_severity(new_severity, reason)
        
        await db.commit()
        
        return {"message": f"Threat escalated to {new_severity} severity"}
        
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to escalate threat: {str(e)}"
        )


@router.get("/stats/summary", response_model=ThreatStatsResponse)
async def get_threat_stats(
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db),
    days: int = Query(default=30, ge=1, le=365, description="Number of days for statistics")
):
    """Get threat statistics summary"""
    try:
        organization_id = current_user["organization_id"]
        start_date = datetime.utcnow() - timedelta(days=days)
        
        # Total threats
        total_query = select(func.count(Threat.id)).join(Email).where(
            and_(
                Email.organization_id == organization_id,
                Threat.created_at >= start_date
            )
        )
        total_result = await db.execute(total_query)
        total_threats = total_result.scalar() or 0
        
        # Threat type distribution
        type_query = select(
            Threat.threat_type,
            func.count(Threat.id).label("count")
        ).join(Email).where(
            and_(
                Email.organization_id == organization_id,
                Threat.created_at >= start_date
            )
        ).group_by(Threat.threat_type)
        
        type_result = await db.execute(type_query)
        type_distribution = {row.threat_type: row.count for row in type_result}
        
        # Severity distribution
        severity_query = select(
            Threat.severity,
            func.count(Threat.id).label("count")
        ).join(Email).where(
            and_(
                Email.organization_id == organization_id,
                Threat.created_at >= start_date
            )
        ).group_by(Threat.severity)
        
        severity_result = await db.execute(severity_query)
        severity_distribution = {row.severity: row.count for row in severity_result}
        
        # Status distribution
        status_query = select(
            Threat.status,
            func.count(Threat.id).label("count")
        ).join(Email).where(
            and_(
                Email.organization_id == organization_id,
                Threat.created_at >= start_date
            )
        ).group_by(Threat.status)
        
        status_result = await db.execute(status_query)
        status_distribution = {row.status: row.count for row in status_result}
        
        # Resolution stats
        resolved_query = select(func.count(Threat.id)).join(Email).where(
            and_(
                Email.organization_id == organization_id,
                Threat.created_at >= start_date,
                Threat.resolved == True
            )
        )
        resolved_result = await db.execute(resolved_query)
        resolved_count = resolved_result.scalar() or 0
        
        false_positive_query = select(func.count(Threat.id)).join(Email).where(
            and_(
                Email.organization_id == organization_id,
                Threat.created_at >= start_date,
                Threat.false_positive == True
            )
        )
        false_positive_result = await db.execute(false_positive_query)
        false_positive_count = false_positive_result.scalar() or 0
        
        # Average risk score
        avg_risk_query = select(func.avg(Threat.risk_score)).join(Email).where(
            and_(
                Email.organization_id == organization_id,
                Threat.created_at >= start_date
            )
        )
        avg_risk_result = await db.execute(avg_risk_query)
        avg_risk_score = avg_risk_result.scalar() or 0.0
        
        return ThreatStatsResponse(
            period_days=days,
            total_threats=total_threats,
            type_distribution=type_distribution,
            severity_distribution=severity_distribution,
            status_distribution=status_distribution,
            resolved_count=resolved_count,
            false_positive_count=false_positive_count,
            avg_risk_score=round(float(avg_risk_score), 3),
            resolution_rate=round((resolved_count / total_threats * 100) if total_threats > 0 else 0.0, 1),
            false_positive_rate=round((false_positive_count / total_threats * 100) if total_threats > 0 else 0.0, 1),
            generated_at=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get threat statistics: {str(e)}"
        )


@router.get("/types")
async def get_threat_types(
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db)
):
    """Get list of all threat types"""
    try:
        organization_id = current_user["organization_id"]
        
        query = select(Threat.threat_type).join(Email).where(
            Email.organization_id == organization_id
        ).distinct()
        
        result = await db.execute(query)
        threat_types = [row[0] for row in result]
        
        # Add standard threat types if not present
        standard_types = ["phishing", "spam", "malware", "suspicious", "business_email_compromise"]
        all_types = list(set(threat_types + standard_types))
        
        return {"threat_types": sorted(all_types)}
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get threat types: {str(e)}"
        )


@router.get("/unresolved")
async def get_unresolved_threats(
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db),
    limit: int = Query(default=20, ge=1, le=100, description="Number of results to return")
):
    """Get unresolved threats that need attention"""
    try:
        organization_id = current_user["organization_id"]
        
        query = select(Threat).join(Email).where(
            and_(
                Email.organization_id == organization_id,
                Threat.resolved == False,
                Threat.false_positive == False,
                Threat.action_required == True
            )
        ).options(selectinload(Threat.email)).order_by(
            desc(Threat.risk_score),
            desc(Threat.created_at)
        ).limit(limit)
        
        result = await db.execute(query)
        threats = result.scalars().all()
        
        return {
            "total_unresolved": len(threats),
            "threats": [ThreatResponse.from_orm(threat) for threat in threats]
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get unresolved threats: {str(e)}"
        ) 

@router.post("/analyze-email-ml")
async def analyze_email_ml(
    email_content: str = Form(..., description="Email content to analyze"),
    current_user: dict = Depends(get_current_user_from_token)
):
    """Analyze email content using ML model for threat detection"""
    try:
        from app.services.enhanced_threat_analyzer import enhanced_analyzer
        
        # Analyze the email using ML model
        analysis_result = await enhanced_analyzer.analyze_email(email_content)
        
        # Create a threat record if spam is detected
        if analysis_result.get('is_spam', False):
            threat_data = {
                'email_content': email_content[:500],  # Truncate for storage
                'threat_type': 'spam',
                'severity': analysis_result.get('threat_level', 'medium'),
                'confidence': analysis_result.get('confidence', 0.0),
                'ml_model_used': analysis_result.get('model_used', 'Unknown'),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
        else:
            threat_data = {
                'email_content': email_content[:500],
                'threat_type': 'safe',
                'severity': 'none',
                'confidence': analysis_result.get('confidence', 0.0),
                'ml_model_used': analysis_result.get('model_used', 'Unknown'),
                'analysis_timestamp': datetime.utcnow().isoformat()
            }
        
        return {
            "success": True,
            "analysis": analysis_result,
            "threat_data": threat_data,
            "user_id": current_user.get("user_id"),
            "organization_id": current_user.get("organization_id")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze email: {str(e)}"
        )

@router.get("/ml-model-info")
async def get_ml_model_info(
    current_user: dict = Depends(get_current_user_from_token)
):
    """Get information about the ML model status"""
    try:
        from app.services.enhanced_threat_analyzer import enhanced_analyzer
        
        model_info = await enhanced_analyzer.get_model_info()
        
        return {
            "success": True,
            "model_info": model_info,
            "user_id": current_user.get("user_id"),
            "organization_id": current_user.get("organization_id")
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get model info: {str(e)}"
        ) 