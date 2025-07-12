"""
Organization Model
Database model for organizations/companies using PhishGuard
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Organization(Base):
    """Organization/Company model"""
    
    __tablename__ = "organizations"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Organization details
    name = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    
    # Contact information
    contact_email = Column(String(255), nullable=True)
    contact_phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    
    # Settings
    is_active = Column(Boolean, default=True, nullable=False)
    max_users = Column(Integer, default=100, nullable=False)
    max_emails_per_day = Column(Integer, default=10000, nullable=False)
    
    # Security settings
    require_2fa = Column(Boolean, default=False, nullable=False)
    password_policy_enabled = Column(Boolean, default=True, nullable=False)
    session_timeout_minutes = Column(Integer, default=60, nullable=False)
    
    # Threat detection settings
    threat_threshold = Column(String(20), default="medium", nullable=False)  # low, medium, high
    auto_quarantine = Column(Boolean, default=True, nullable=False)
    send_alerts = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")
    emails = relationship("Email", back_populates="organization", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Organization(id={self.id}, name='{self.name}', domain='{self.domain}')>"
    
    def to_dict(self):
        """Convert organization to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "domain": self.domain,
            "description": self.description,
            "contact_email": self.contact_email,
            "contact_phone": self.contact_phone,
            "address": self.address,
            "is_active": self.is_active,
            "max_users": self.max_users,
            "max_emails_per_day": self.max_emails_per_day,
            "require_2fa": self.require_2fa,
            "password_policy_enabled": self.password_policy_enabled,
            "session_timeout_minutes": self.session_timeout_minutes,
            "threat_threshold": self.threat_threshold,
            "auto_quarantine": self.auto_quarantine,
            "send_alerts": self.send_alerts,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        } 