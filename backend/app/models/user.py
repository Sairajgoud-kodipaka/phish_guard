"""
User Model
Database model for users in the PhishGuard system
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """User model for authentication and authorization"""
    
    __tablename__ = "users"
    
    # Primary key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # User information
    full_name = Column(String(255), nullable=True)
    job_title = Column(String(100), nullable=True)
    department = Column(String(100), nullable=True)
    phone = Column(String(50), nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Security
    failed_login_attempts = Column(Integer, default=0, nullable=False)
    last_login = Column(DateTime(timezone=True), nullable=True)
    password_changed_at = Column(DateTime(timezone=True), nullable=True)
    
    # Two-factor authentication
    totp_secret = Column(String(255), nullable=True)
    is_2fa_enabled = Column(Boolean, default=False, nullable=False)
    backup_codes = Column(JSON, nullable=True)
    
    # Permissions and roles
    permissions = Column(JSON, default=list, nullable=False)
    role = Column(String(50), default="user", nullable=False)  # user, admin, analyst, viewer
    
    # Settings
    timezone = Column(String(50), default="UTC", nullable=False)
    language = Column(String(10), default="en", nullable=False)
    email_notifications = Column(Boolean, default=True, nullable=False)
    
    # Organization relationship
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    
    # Relationships
    organization = relationship("Organization", back_populates="users")
    
    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
    
    def to_dict(self, include_sensitive=False):
        """Convert user to dictionary"""
        data = {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "full_name": self.full_name,
            "job_title": self.job_title,
            "department": self.department,
            "phone": self.phone,
            "is_active": self.is_active,
            "is_superuser": self.is_superuser,
            "is_verified": self.is_verified,
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_2fa_enabled": self.is_2fa_enabled,
            "permissions": self.permissions,
            "role": self.role,
            "timezone": self.timezone,
            "language": self.language,
            "email_notifications": self.email_notifications,
            "organization_id": self.organization_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        
        if include_sensitive:
            data.update({
                "failed_login_attempts": self.failed_login_attempts,
                "password_changed_at": self.password_changed_at.isoformat() if self.password_changed_at else None,
            })
        
        return data
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission"""
        if self.is_superuser:
            return True
        return permission in (self.permissions or [])
    
    def add_permission(self, permission: str):
        """Add permission to user"""
        if not self.permissions:
            self.permissions = []
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def remove_permission(self, permission: str):
        """Remove permission from user"""
        if self.permissions and permission in self.permissions:
            self.permissions.remove(permission)
    
    @property
    def is_admin(self) -> bool:
        """Check if user is an admin"""
        return self.role == "admin" or self.is_superuser
    
    @property
    def is_analyst(self) -> bool:
        """Check if user is an analyst"""
        return self.role in ["analyst", "admin"] or self.is_superuser
    
    def can_manage_users(self) -> bool:
        """Check if user can manage other users"""
        return self.is_superuser or self.has_permission("manage_users")
    
    def can_view_reports(self) -> bool:
        """Check if user can view reports"""
        return self.has_permission("view_reports") or self.is_analyst
    
    def can_manage_threats(self) -> bool:
        """Check if user can manage threats"""
        return self.has_permission("manage_threats") or self.is_analyst 