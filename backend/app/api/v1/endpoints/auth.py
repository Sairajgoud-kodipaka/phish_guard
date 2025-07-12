"""
Authentication API Endpoints
Login, logout, token refresh, and user management
"""

from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.sql import func

from app.core.database import get_async_db
from app.core.security import (
    create_access_token, 
    create_refresh_token,
    verify_password,
    get_current_user_from_token,
    get_password_hash,
    verify_token,
    check_rate_limit
)
from app.core.config import settings
from app.core.logger import security_logger
from app.models.user import User
from app.models.organization import Organization
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    TokenRefreshRequest,
    TokenRefreshResponse,
    UserCreateRequest,
    UserResponse,
    ChangePasswordRequest
)

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_db),
    _: bool = Depends(check_rate_limit)
):
    """User login endpoint"""
    client_ip = request.client.host if request.client else "unknown"
    
    try:
        # Find user by email or username
        stmt = select(User).where(
            (User.email == form_data.username) | 
            (User.username == form_data.username)
        )
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            security_logger.log_auth_attempt(form_data.username, False, client_ip)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email/username or password"
            )
        
        # Verify password
        if not verify_password(form_data.password, user.hashed_password):
            user.failed_login_attempts += 1
            await db.commit()
            
            security_logger.log_auth_attempt(user.email, False, client_ip)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email/username or password"
            )
        
        # Check if user is active
        if not user.is_active:
            security_logger.log_auth_attempt(user.email, False, client_ip)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Account is deactivated"
            )
        
        # Reset failed login attempts and update last login
        user.failed_login_attempts = 0
        user.last_login = func.now()
        await db.commit()
        
        # Create tokens with user information
        additional_claims = {
            "email": user.email,
            "username": user.username,
            "is_superuser": user.is_superuser,
            "organization_id": user.organization_id,
            "permissions": user.permissions
        }
        
        access_token = create_access_token(
            subject=str(user.id),
            additional_claims=additional_claims
        )
        refresh_token = create_refresh_token(subject=str(user.id))
        
        security_logger.log_auth_attempt(user.email, True, client_ip)
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            user=UserResponse.from_orm(user)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        security_logger.log_suspicious_activity(
            form_data.username, 
            "login_error", 
            {"error": str(e), "ip": client_ip}
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post("/refresh", response_model=TokenRefreshResponse)
async def refresh_token(
    request: TokenRefreshRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """Refresh access token using refresh token"""
    try:
        # Verify refresh token
        payload = verify_token(request.refresh_token)
        if not payload or payload.get("type") != "refresh_token":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Get user from database
        stmt = select(User).where(User.id == int(user_id))
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found or inactive"
            )
        
        # Create new access token
        additional_claims = {
            "email": user.email,
            "username": user.username,
            "is_superuser": user.is_superuser,
            "organization_id": user.organization_id,
            "permissions": user.permissions
        }
        
        new_access_token = create_access_token(
            subject=str(user.id),
            additional_claims=additional_claims
        )
        
        return TokenRefreshResponse(
            access_token=new_access_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )


@router.post("/logout")
async def logout(current_user: dict = Depends(get_current_user_from_token)):
    """User logout endpoint"""
    # In a real implementation, you might want to blacklist the token
    # For now, we'll just return success
    security_logger.log_auth_attempt(current_user.get("email"), True, None)
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db)
):
    """Get current user information"""
    try:
        stmt = select(User).where(User.id == int(current_user["user_id"]))
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserResponse.from_orm(user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user information"
        )


@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: dict = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_db)
):
    """Change user password"""
    try:
        # Get user from database
        stmt = select(User).where(User.id == int(current_user["user_id"]))
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Verify current password
        if not verify_password(request.current_password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Current password is incorrect"
            )
        
        # Update password
        user.hashed_password = get_password_hash(request.new_password)
        user.password_changed_at = func.now()
        await db.commit()
        
        security_logger.log_auth_attempt(
            user.email, 
            True, 
            None, 
            "password_changed"
        )
        
        return {"message": "Password changed successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to change password"
        )


@router.post("/register", response_model=UserResponse)
async def register_user(
    request: UserCreateRequest,
    db: AsyncSession = Depends(get_async_db)
):
    """Register new user (admin only in production)"""
    try:
        # Check if user already exists
        stmt = select(User).where(
            (User.email == request.email) | 
            (User.username == request.username)
        )
        result = await db.execute(stmt)
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email or username already exists"
            )
        
        # Get or create organization
        org_stmt = select(Organization).where(Organization.id == request.organization_id)
        org_result = await db.execute(org_stmt)
        organization = org_result.scalar_one_or_none()
        
        if not organization:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Organization not found"
            )
        
        # Create new user
        new_user = User(
            email=request.email,
            username=request.username,
            hashed_password=get_password_hash(request.password),
            full_name=request.full_name,
            job_title=request.job_title,
            department=request.department,
            role=request.role,
            organization_id=request.organization_id
        )
        
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        return UserResponse.from_orm(new_user)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to register user"
        ) 