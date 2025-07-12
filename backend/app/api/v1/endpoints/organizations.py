"""
Organization API Endpoints
Organization management endpoints
"""

from fastapi import APIRouter, Depends
from app.core.security import get_current_user_from_token

router = APIRouter()


@router.get("/")
async def get_organizations(current_user: dict = Depends(get_current_user_from_token)):
    """Get organizations (placeholder)"""
    return {"message": "Organizations endpoint - coming soon"} 