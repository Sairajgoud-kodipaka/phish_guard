"""
User API Endpoints
User management endpoints
"""

from fastapi import APIRouter, Depends
from app.core.security import get_current_user_from_token

router = APIRouter()


@router.get("/list")
async def get_users(current_user: dict = Depends(get_current_user_from_token)):
    """Get users (placeholder)"""
    return {"message": "Users endpoint - coming soon"} 