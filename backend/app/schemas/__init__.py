"""
Schemas package initialization
Import all Pydantic schemas for PhishGuard API
"""

from .auth import (
    LoginRequest,
    LoginResponse, 
    TokenRefreshRequest,
    TokenRefreshResponse,
    UserCreateRequest,
    UserResponse,
    ChangePasswordRequest
)

from .dashboard import (
    DashboardStats,
    ThreatTimelineItem,
    EmailActivityItem,
    ThreatDistribution,
    RecentActivity
)

from .email import (
    EmailBase,
    EmailCreateRequest,
    EmailResponse,
    EmailDetailResponse,
    EmailAnalysisResponse,
    BatchAnalysisRequest,
    BatchAnalysisResponse,
    EmailStatsResponse,
    EmailFilterParams,
    FalsePositiveRequest,
    EmailActionRequest,
    EmailSearchRequest,
    EmailSearchResponse,
    ThreatInfo
)

from .threat import (
    ThreatBase,
    ThreatCreateRequest,
    ThreatUpdateRequest,
    ThreatResponse,
    ThreatDetailResponse,
    ThreatStatsResponse,
    ThreatFilterParams,
    ThreatActionRequest,
    ThreatSearchRequest,
    ThreatSearchResponse,
    InvestigationRequest,
    ResolutionRequest,
    FalsePositiveRequest as ThreatFalsePositiveRequest,
    EscalationRequest,
    EmailInfo
)

__all__ = [
    # Auth schemas
    "LoginRequest",
    "LoginResponse", 
    "TokenRefreshRequest",
    "TokenRefreshResponse",
    "UserCreateRequest",
    "UserResponse",
    "ChangePasswordRequest",
    
    # Dashboard schemas
    "DashboardStats",
    "ThreatTimelineItem",
    "EmailActivityItem", 
    "ThreatDistribution",
    "RecentActivity",
    
    # Email schemas
    "EmailBase",
    "EmailCreateRequest",
    "EmailResponse",
    "EmailDetailResponse",
    "EmailAnalysisResponse",
    "BatchAnalysisRequest",
    "BatchAnalysisResponse",
    "EmailStatsResponse",
    "EmailFilterParams",
    "FalsePositiveRequest",
    "EmailActionRequest",
    "EmailSearchRequest",
    "EmailSearchResponse",
    "ThreatInfo",
    
    # Threat schemas
    "ThreatBase",
    "ThreatCreateRequest", 
    "ThreatUpdateRequest",
    "ThreatResponse",
    "ThreatDetailResponse",
    "ThreatStatsResponse",
    "ThreatFilterParams",
    "ThreatActionRequest",
    "ThreatSearchRequest",
    "ThreatSearchResponse",
    "InvestigationRequest",
    "ResolutionRequest",
    "ThreatFalsePositiveRequest",
    "EscalationRequest",
    "EmailInfo"
] 