"""
Email Model
Database model for emails processed by PhishGuard
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Email(Base):
    """Email model for storing email data and analysis results"""
    
    __tablename__ = "emails"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Email identifiers
    message_id = Column(String(255), nullable=False, index=True)
    subject = Column(Text, nullable=True)
    sender_email = Column(String(255), nullable=False, index=True)
    sender_name = Column(String(255), nullable=True)
    recipient_email = Column(String(255), nullable=False, index=True)
    recipient_name = Column(String(255), nullable=True)
    
    # Email metadata
    date_sent = Column(DateTime(timezone=True), nullable=True)
    date_received = Column(DateTime(timezone=True), nullable=False, index=True)
    email_size = Column(Integer, nullable=True)  # Size in bytes
    
    # Email content
    body_text = Column(Text, nullable=True)
    body_html = Column(Text, nullable=True)
    headers = Column(JSON, nullable=True)
    
    # URLs and attachments
    urls = Column(JSON, default=list, nullable=False)  # List of URLs found in email
    attachments = Column(JSON, default=list, nullable=False)  # List of attachment info
    
    # SPF/DKIM/DMARC
    spf_result = Column(String(20), nullable=True)  # pass, fail, neutral, none
    dkim_result = Column(String(20), nullable=True)  # pass, fail, none
    dmarc_result = Column(String(20), nullable=True)  # pass, fail, none
    
    # Processing status
    status = Column(String(20), default="pending", nullable=False, index=True)  # pending, processing, completed, failed
    processed_at = Column(DateTime(timezone=True), nullable=True)
    processing_time = Column(Float, nullable=True)  # Processing time in seconds
    
    # Threat analysis results
    threat_score = Column(Float, default=0.0, nullable=False, index=True)  # 0.0 to 1.0
    threat_level = Column(String(20), default="clean", nullable=False, index=True)  # clean, low, medium, high, critical
    is_phishing = Column(Boolean, default=False, nullable=False)
    is_spam = Column(Boolean, default=False, nullable=False)
    is_malware = Column(Boolean, default=False, nullable=False)
    
    # Analysis details
    analysis_results = Column(JSON, default=dict, nullable=False)
    ml_predictions = Column(JSON, default=dict, nullable=False)
    confidence_score = Column(Float, default=0.0, nullable=False)
    
    # Action taken
    action_taken = Column(String(50), default="none", nullable=False)  # none, quarantine, block, allow
    quarantined = Column(Boolean, default=False, nullable=False)
    user_reported = Column(Boolean, default=False, nullable=False)
    false_positive = Column(Boolean, default=False, nullable=False)
    
    # External analysis
    virustotal_scan_id = Column(String(255), nullable=True)
    virustotal_results = Column(JSON, nullable=True)
    
    # Organization relationship
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="emails")
    threats = relationship("Threat", back_populates="email", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Email(id={self.id}, subject='{self.subject[:50]}...', sender='{self.sender_email}')>"
    
    def to_dict(self, include_content=False):
        """Convert email to dictionary"""
        data = {
            "id": self.id,
            "message_id": self.message_id,
            "subject": self.subject,
            "sender_email": self.sender_email,
            "sender_name": self.sender_name,
            "recipient_email": self.recipient_email,
            "recipient_name": self.recipient_name,
            "date_sent": self.date_sent.isoformat() if self.date_sent else None,
            "date_received": self.date_received.isoformat() if self.date_received else None,
            "email_size": self.email_size,
            "urls": self.urls,
            "attachments": self.attachments,
            "spf_result": self.spf_result,
            "dkim_result": self.dkim_result,
            "dmarc_result": self.dmarc_result,
            "status": self.status,
            "processed_at": self.processed_at.isoformat() if self.processed_at else None,
            "processing_time": self.processing_time,
            "threat_score": self.threat_score,
            "threat_level": self.threat_level,
            "is_phishing": self.is_phishing,
            "is_spam": self.is_spam,
            "is_malware": self.is_malware,
            "confidence_score": self.confidence_score,
            "action_taken": self.action_taken,
            "quarantined": self.quarantined,
            "user_reported": self.user_reported,
            "false_positive": self.false_positive,
            "organization_id": self.organization_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_content:
            data.update({
                "body_text": self.body_text,
                "body_html": self.body_html,
                "headers": self.headers,
                "analysis_results": self.analysis_results,
                "ml_predictions": self.ml_predictions,
                "virustotal_results": self.virustotal_results,
            })
        
        return data
    
    @property
    def is_threat(self) -> bool:
        """Check if email is classified as a threat"""
        return self.threat_level in ["medium", "high", "critical"]
    
    @property
    def is_safe(self) -> bool:
        """Check if email is classified as safe"""
        return self.threat_level in ["clean", "low"] and not self.is_phishing
    
    def get_threat_indicators(self) -> list:
        """Get list of threat indicators for this email"""
        indicators = []
        
        if self.is_phishing:
            indicators.append("phishing")
        if self.is_spam:
            indicators.append("spam")
        if self.is_malware:
            indicators.append("malware")
        if self.spf_result == "fail":
            indicators.append("spf_fail")
        if self.dkim_result == "fail":
            indicators.append("dkim_fail")
        if self.dmarc_result == "fail":
            indicators.append("dmarc_fail")
        
        return indicators
    
    def update_threat_analysis(self, 
                             threat_score: float,
                             threat_level: str,
                             analysis_results: dict = None,
                             ml_predictions: dict = None):
        """Update threat analysis results"""
        self.threat_score = threat_score
        self.threat_level = threat_level
        self.confidence_score = analysis_results.get("confidence", 0.0) if analysis_results else 0.0
        
        # Update boolean flags based on analysis
        if analysis_results:
            self.is_phishing = analysis_results.get("is_phishing", False)
            self.is_spam = analysis_results.get("is_spam", False)
            self.is_malware = analysis_results.get("is_malware", False)
        
        if analysis_results:
            self.analysis_results = analysis_results
        if ml_predictions:
            self.ml_predictions = ml_predictions
        
        self.processed_at = func.now()
        self.status = "completed"
    
    def mark_as_false_positive(self):
        """Mark email as false positive"""
        self.false_positive = True
        self.threat_level = "clean"
        self.threat_score = 0.0
        self.is_phishing = False
        self.is_spam = False
        self.is_malware = False
        self.quarantined = False
        self.action_taken = "allow"
    
    def quarantine(self):
        """Quarantine the email"""
        self.quarantined = True
        self.action_taken = "quarantine"
    
    def release_from_quarantine(self):
        """Release email from quarantine"""
        self.quarantined = False
        self.action_taken = "allow" 