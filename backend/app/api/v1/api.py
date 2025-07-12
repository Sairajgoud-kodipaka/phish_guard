"""
Main API Router
Combines all API endpoints for PhishGuard v1 API
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, dashboard, emails, threats, users, organizations

# Create main API router
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

api_router.include_router(
    dashboard.router,
    prefix="/dashboard",
    tags=["dashboard"]
)

api_router.include_router(
    emails.router,
    prefix="/emails",
    tags=["emails"]
)

api_router.include_router(
    threats.router,
    prefix="/threats",
    tags=["threats"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    organizations.router,
    prefix="/organizations",
    tags=["organizations"]
) 