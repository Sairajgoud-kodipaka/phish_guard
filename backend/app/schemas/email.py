"""
Email Schemas
Pydantic models for email-related API requests and responses
"""

from typing import List, Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, EmailStr


class EmailBase(BaseModel):
    """Base email schema with common fields"""
    subject: Optional[str] = Field(None, description="Email subject")
    sender_email: str = Field(..., description="Sender email address")
    sender_name: Optional[str] = Field(None, description="Sender display name")
    recipient_email: str = Field(..., description="Recipient email address")
    recipient_name: Optional[str] = Field(None, description="Recipient display name")


class EmailCreateRequest(EmailBase):
    """Email creation request schema"""
    message_id: str = Field(..., description="Email message ID")
    date_sent: Optional[datetime] = Field(None, description="Date email was sent")
    body_text: Optional[str] = Field(None, description="Plain text body")
    body_html: Optional[str] = Field(None, description="HTML body")
    headers: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Email headers")
    urls: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="URLs found in email")
    attachments: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Attachments")


class EmailTextAnalysisRequest(BaseModel):
    """Email text analysis request schema"""
    content: str = Field(..., description="Raw email content to analyze")


class ThreatInfo(BaseModel):
    """Threat information schema"""
    id: int
    threat_type: str
    severity: str
    title: str
    description: Optional[str]
    confidence_score: float
    risk_score: float
    status: str
    
    class Config:
        from_attributes = True


class EmailResponse(EmailBase):
    """Email response schema"""
    id: int
    message_id: str
    date_sent: Optional[datetime]
    date_received: datetime
    email_size: Optional[int]
    
    # Email content (limited in list view)
    body_text: Optional[str] = Field(None, description="Plain text body (truncated in list view)")
    body_html: Optional[str] = Field(None, description="HTML body (limited in list view)")
    
    # URLs and attachments
    urls: List[Dict[str, Any]] = Field(default_factory=list)
    attachments: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Authentication results
    spf_result: Optional[str]
    dkim_result: Optional[str]
    dmarc_result: Optional[str]
    
    # Processing status
    status: str
    processed_at: Optional[datetime]
    processing_time: Optional[float]
    
    # Threat analysis results
    threat_score: float
    threat_level: str
    is_phishing: bool
    is_spam: bool
    is_malware: bool
    confidence_score: float
    
    # Actions
    action_taken: str
    quarantined: bool
    user_reported: bool
    false_positive: bool
    
    # Organization
    organization_id: int
    
    # Associated threats
    threats: List[ThreatInfo] = Field(default_factory=list)
    
    # Timestamps
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class EmailDetailResponse(EmailResponse):
    """Detailed email response with full content"""
    headers: Dict[str, Any] = Field(default_factory=dict)
    analysis_results: Dict[str, Any] = Field(default_factory=dict)
    ml_predictions: Dict[str, Any] = Field(default_factory=dict)


class EmailAnalysisResponse(BaseModel):
    """Email analysis result schema"""
    email_id: int
    threat_score: float = Field(..., ge=0.0, le=1.0, description="Overall threat score (0-1)")
    threat_level: str = Field(..., description="Threat level: clean, low, medium, high, critical")
    is_phishing: bool
    is_spam: bool
    is_malware: bool
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Analysis confidence (0-1)")
    recommended_action: str = Field(..., description="Recommended action: allow, flag, quarantine, block")
    threat_indicators: List[str] = Field(default_factory=list, description="List of threat indicators found")
    analysis_summary: Dict[str, Any] = Field(default_factory=dict, description="Detailed analysis results")
    url_scan_results: Optional[Dict[str, Any]] = Field(None, description="URL scanning results")
    processing_time: float = Field(..., description="Analysis processing time in seconds")


class BatchAnalysisRequest(BaseModel):
    """Batch email analysis request"""
    files: List[str] = Field(..., description="List of file paths or base64 encoded content")
    analysis_options: Optional[Dict[str, Any]] = Field(default_factory=dict)


class BatchAnalysisResponse(BaseModel):
    """Batch analysis response"""
    total_files: int
    successful: int
    failed: int
    results: List[Dict[str, Any]]
    processing_time: float


class EmailStatsResponse(BaseModel):
    """Email statistics response"""
    period_days: int
    total_emails: int
    threat_distribution: Dict[str, int] = Field(description="Count by threat level")
    status_distribution: Dict[str, int] = Field(description="Count by processing status")
    action_distribution: Dict[str, int] = Field(description="Count by action taken")
    generated_at: str


class EmailFilterParams(BaseModel):
    """Email filtering parameters"""
    threat_level: Optional[str] = Field(None, description="Filter by threat level")
    status: Optional[str] = Field(None, description="Filter by processing status")
    sender: Optional[str] = Field(None, description="Filter by sender email")
    start_date: Optional[datetime] = Field(None, description="Filter emails after this date")
    end_date: Optional[datetime] = Field(None, description="Filter emails before this date")
    is_quarantined: Optional[bool] = Field(None, description="Filter by quarantine status")
    has_attachments: Optional[bool] = Field(None, description="Filter emails with attachments")
    has_urls: Optional[bool] = Field(None, description="Filter emails with URLs")


class FalsePositiveRequest(BaseModel):
    """False positive report request"""
    reason: str = Field(..., description="Reason for marking as false positive")
    notes: Optional[str] = Field(None, description="Additional notes")


class EmailActionRequest(BaseModel):
    """Email action request (quarantine, release, etc.)"""
    action: str = Field(..., description="Action to perform")
    reason: Optional[str] = Field(None, description="Reason for action")
    notify_user: bool = Field(default=False, description="Notify the user of the action")


class EmailSearchRequest(BaseModel):
    """Email search request"""
    query: str = Field(..., description="Search query")
    fields: Optional[List[str]] = Field(default=["subject", "body_text", "sender_email"], 
                                       description="Fields to search in")
    filters: Optional[EmailFilterParams] = Field(None, description="Additional filters")
    limit: int = Field(default=50, ge=1, le=100, description="Maximum results to return")


class EmailSearchResponse(BaseModel):
    """Email search response"""
    total_results: int
    results: List[EmailResponse]
    search_time: float
    query: str 