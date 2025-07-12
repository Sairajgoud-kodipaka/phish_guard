"""
Threat Model
Database model for detailed threat information
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON, Float
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Threat(Base):
    """Threat model for detailed threat analysis and tracking"""
    
    __tablename__ = "threats"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Threat classification
    threat_type = Column(String(50), nullable=False, index=True)  # phishing, spam, malware, suspicious
    threat_category = Column(String(100), nullable=True)  # credential_theft, business_email_compromise, etc.
    severity = Column(String(20), default="medium", nullable=False)  # low, medium, high, critical
    
    # Threat details
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    indicators = Column(JSON, default=list, nullable=False)  # List of threat indicators
    tactics = Column(JSON, default=list, nullable=False)  # MITRE ATT&CK tactics
    techniques = Column(JSON, default=list, nullable=False)  # MITRE ATT&CK techniques
    
    # Detection information
    detection_method = Column(String(100), nullable=False)  # ml_model, rule_based, url_reputation, etc.
    confidence_score = Column(Float, default=0.0, nullable=False)
    risk_score = Column(Float, default=0.0, nullable=False)
    
    # Analysis details
    analysis_details = Column(JSON, default=dict, nullable=False)
    ml_model_results = Column(JSON, default=dict, nullable=False)
    external_analysis = Column(JSON, default=dict, nullable=False)
    
    # Status and actions
    status = Column(String(20), default="detected", nullable=False)  # detected, investigating, confirmed, false_positive, resolved
    action_required = Column(Boolean, default=True, nullable=False)
    action_taken = Column(String(100), nullable=True)
    remediation_steps = Column(JSON, default=list, nullable=False)
    
    # Investigation details
    investigated_by = Column(String(255), nullable=True)  # User who investigated
    investigation_notes = Column(Text, nullable=True)
    investigated_at = Column(DateTime(timezone=True), nullable=True)
    
    # Resolution information
    resolved = Column(Boolean, default=False, nullable=False)
    resolved_by = Column(String(255), nullable=True)
    resolved_at = Column(DateTime(timezone=True), nullable=True)
    resolution_notes = Column(Text, nullable=True)
    
    # False positive tracking
    false_positive = Column(Boolean, default=False, nullable=False)
    false_positive_reason = Column(Text, nullable=True)
    reported_by = Column(String(255), nullable=True)
    
    # Email relationship
    email_id = Column(Integer, ForeignKey("emails.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    email = relationship("Email", back_populates="threats")
    
    def __repr__(self):
        return f"<Threat(id={self.id}, type='{self.threat_type}', severity='{self.severity}')>"
    
    def to_dict(self, include_details=False):
        """Convert threat to dictionary"""
        data = {
            "id": self.id,
            "threat_type": self.threat_type,
            "threat_category": self.threat_category,
            "severity": self.severity,
            "title": self.title,
            "description": self.description,
            "indicators": self.indicators,
            "tactics": self.tactics,
            "techniques": self.techniques,
            "detection_method": self.detection_method,
            "confidence_score": self.confidence_score,
            "risk_score": self.risk_score,
            "status": self.status,
            "action_required": self.action_required,
            "action_taken": self.action_taken,
            "remediation_steps": self.remediation_steps,
            "investigated_by": self.investigated_by,
            "investigated_at": self.investigated_at.isoformat() if self.investigated_at else None,
            "resolved": self.resolved,
            "resolved_by": self.resolved_by,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "false_positive": self.false_positive,
            "false_positive_reason": self.false_positive_reason,
            "reported_by": self.reported_by,
            "email_id": self.email_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_details:
            data.update({
                "analysis_details": self.analysis_details,
                "ml_model_results": self.ml_model_results,
                "external_analysis": self.external_analysis,
                "investigation_notes": self.investigation_notes,
                "resolution_notes": self.resolution_notes,
            })
        
        return data
    
    @property
    def is_critical(self) -> bool:
        """Check if threat is critical severity"""
        return self.severity == "critical"
    
    @property
    def is_high_risk(self) -> bool:
        """Check if threat is high risk"""
        return self.severity in ["high", "critical"] or self.risk_score >= 0.8
    
    @property
    def needs_investigation(self) -> bool:
        """Check if threat needs investigation"""
        return (self.status == "detected" and 
                self.action_required and 
                not self.false_positive and 
                not self.resolved)
    
    def add_indicator(self, indicator: str):
        """Add threat indicator"""
        if not self.indicators:
            self.indicators = []
        if indicator not in self.indicators:
            self.indicators.append(indicator)
    
    def add_tactic(self, tactic: str):
        """Add MITRE ATT&CK tactic"""
        if not self.tactics:
            self.tactics = []
        if tactic not in self.tactics:
            self.tactics.append(tactic)
    
    def add_technique(self, technique: str):
        """Add MITRE ATT&CK technique"""
        if not self.techniques:
            self.techniques = []
        if technique not in self.techniques:
            self.techniques.append(technique)
    
    def start_investigation(self, investigator: str):
        """Start investigation of the threat"""
        self.status = "investigating"
        self.investigated_by = investigator
        self.investigated_at = func.now()
    
    def confirm_threat(self, investigator: str, notes: str = None):
        """Confirm threat as legitimate"""
        self.status = "confirmed"
        self.investigated_by = investigator
        self.investigated_at = func.now()
        if notes:
            self.investigation_notes = notes
    
    def mark_false_positive(self, investigator: str, reason: str = None):
        """Mark threat as false positive"""
        self.false_positive = True
        self.status = "false_positive"
        self.action_required = False
        self.investigated_by = investigator
        self.investigated_at = func.now()
        if reason:
            self.false_positive_reason = reason
    
    def resolve(self, resolver: str, notes: str = None, action_taken: str = None):
        """Resolve the threat"""
        self.resolved = True
        self.resolved_by = resolver
        self.resolved_at = func.now()
        self.status = "resolved"
        self.action_required = False
        if notes:
            self.resolution_notes = notes
        if action_taken:
            self.action_taken = action_taken
    
    def escalate_severity(self, new_severity: str, reason: str = None):
        """Escalate threat severity"""
        old_severity = self.severity
        self.severity = new_severity
        if reason:
            if not self.investigation_notes:
                self.investigation_notes = ""
            self.investigation_notes += f"\nSeverity escalated from {old_severity} to {new_severity}: {reason}"
    
    def update_risk_score(self, new_score: float):
        """Update risk score based on new analysis"""
        self.risk_score = max(0.0, min(1.0, new_score))  # Clamp between 0 and 1
        
        # Auto-update severity based on risk score
        if self.risk_score >= 0.9:
            self.severity = "critical"
        elif self.risk_score >= 0.7:
            self.severity = "high"
        elif self.risk_score >= 0.4:
            self.severity = "medium"
        else:
            self.severity = "low" 