"""
Threat Schemas
Pydantic models for threat-related API requests and responses
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ThreatBase(BaseModel):
    """Base threat schema with common fields"""
    threat_type: str = Field(..., description="Type of threat (phishing, spam, malware, etc.)")
    threat_category: Optional[str] = Field(None, description="Specific threat category")
    severity: str = Field(..., description="Severity level: low, medium, high, critical")
    title: str = Field(..., description="Threat title or summary")
    description: Optional[str] = Field(None, description="Detailed threat description")


class ThreatCreateRequest(ThreatBase):
    """Threat creation request schema"""
    indicators: Optional[List[str]] = Field(default_factory=list, description="Threat indicators")
    tactics: Optional[List[str]] = Field(default_factory=list, description="MITRE ATT&CK tactics")
    techniques: Optional[List[str]] = Field(default_factory=list, description="MITRE ATT&CK techniques")
    detection_method: str = Field(..., description="Detection method used")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Detection confidence")
    risk_score: float = Field(..., ge=0.0, le=1.0, description="Risk score")
    email_id: int = Field(..., description="Associated email ID")


class ThreatUpdateRequest(BaseModel):
    """Threat update request schema"""
    severity: Optional[str] = Field(None, description="Updated severity level")
    status: Optional[str] = Field(None, description="Updated status")
    investigation_notes: Optional[str] = Field(None, description="Investigation notes")
    resolution_notes: Optional[str] = Field(None, description="Resolution notes")
    action_taken: Optional[str] = Field(None, description="Action taken")


class EmailInfo(BaseModel):
    """Basic email information for threat response"""
    id: int
    subject: Optional[str]
    sender_email: str
    sender_name: Optional[str]
    date_received: datetime
    threat_score: float
    threat_level: str
    
    class Config:
        from_attributes = True


class ThreatResponse(ThreatBase):
    """Threat response schema"""
    id: int
    
    # Threat details
    indicators: List[str] = Field(default_factory=list)
    tactics: List[str] = Field(default_factory=list)
    techniques: List[str] = Field(default_factory=list)
    
    # Detection information
    detection_method: str
    confidence_score: float
    risk_score: float
    
    # Analysis details (limited in list view)
    analysis_details: Optional[Dict[str, Any]] = Field(None, description="Detailed analysis")
    ml_model_results: Optional[Dict[str, Any]] = Field(None, description="ML model results")
    external_analysis: Optional[Dict[str, Any]] = Field(None, description="External analysis")
    
    # Status and actions
    status: str
    action_required: bool
    action_taken: Optional[str]
    remediation_steps: List[str] = Field(default_factory=list)
    
    # Investigation details
    investigated_by: Optional[str]
    investigation_notes: Optional[str]
    investigated_at: Optional[datetime]
    
    # Resolution information
    resolved: bool
    resolved_by: Optional[str]
    resolved_at: Optional[datetime]
    resolution_notes: Optional[str]
    
    # False positive tracking
    false_positive: bool
    false_positive_reason: Optional[str]
    reported_by: Optional[str]
    
    # Associated email
    email_id: int
    email: Optional[EmailInfo] = Field(None, description="Associated email information")
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ThreatDetailResponse(ThreatResponse):
    """Detailed threat response with full analysis data"""
    analysis_details: Dict[str, Any] = Field(default_factory=dict)
    ml_model_results: Dict[str, Any] = Field(default_factory=dict)
    external_analysis: Dict[str, Any] = Field(default_factory=dict)


class ThreatStatsResponse(BaseModel):
    """Threat statistics response"""
    period_days: int
    total_threats: int
    type_distribution: Dict[str, int] = Field(description="Count by threat type")
    severity_distribution: Dict[str, int] = Field(description="Count by severity")
    status_distribution: Dict[str, int] = Field(description="Count by status")
    resolved_count: int
    false_positive_count: int
    avg_risk_score: float
    resolution_rate: float = Field(description="Percentage of resolved threats")
    false_positive_rate: float = Field(description="Percentage of false positives")
    generated_at: str


class ThreatFilterParams(BaseModel):
    """Threat filtering parameters"""
    threat_type: Optional[str] = Field(None, description="Filter by threat type")
    severity: Optional[str] = Field(None, description="Filter by severity")
    status: Optional[str] = Field(None, description="Filter by status")
    resolved: Optional[bool] = Field(None, description="Filter by resolution status")
    false_positive: Optional[bool] = Field(None, description="Filter by false positive status")
    start_date: Optional[datetime] = Field(None, description="Filter threats after this date")
    end_date: Optional[datetime] = Field(None, description="Filter threats before this date")
    min_risk_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Minimum risk score")
    max_risk_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Maximum risk score")


class ThreatActionRequest(BaseModel):
    """Threat action request"""
    action: str = Field(..., description="Action to perform (investigate, confirm, resolve, etc.)")
    notes: Optional[str] = Field(None, description="Action notes")
    severity: Optional[str] = Field(None, description="New severity (for escalation)")


class ThreatSearchRequest(BaseModel):
    """Threat search request"""
    query: str = Field(..., description="Search query")
    fields: Optional[List[str]] = Field(default=["title", "description", "indicators"], 
                                       description="Fields to search in")
    filters: Optional[ThreatFilterParams] = Field(None, description="Additional filters")
    limit: int = Field(default=50, ge=1, le=100, description="Maximum results to return")


class ThreatSearchResponse(BaseModel):
    """Threat search response"""
    total_results: int
    results: List[ThreatResponse]
    search_time: float
    query: str


class InvestigationRequest(BaseModel):
    """Investigation start request"""
    notes: Optional[str] = Field(None, description="Initial investigation notes")
    priority: Optional[str] = Field(default="normal", description="Investigation priority")


class ResolutionRequest(BaseModel):
    """Threat resolution request"""
    resolution_notes: str = Field(..., description="Resolution notes")
    action_taken: Optional[str] = Field(None, description="Action taken to resolve")
    remediation_steps: Optional[List[str]] = Field(None, description="Remediation steps taken")


class FalsePositiveRequest(BaseModel):
    """False positive marking request"""
    reason: str = Field(..., description="Reason for marking as false positive")
    notes: Optional[str] = Field(None, description="Additional notes")


class EscalationRequest(BaseModel):
    """Threat escalation request"""
    new_severity: str = Field(..., description="New severity level")
    reason: str = Field(..., description="Reason for escalation")
    notify_team: bool = Field(default=True, description="Notify security team of escalation") 