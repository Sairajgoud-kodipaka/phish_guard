"""
PhishGuard Backend Security
Authentication, authorization, and security utilities
"""

from datetime import datetime, timedelta
from typing import Optional, Union, Any
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import secrets
import structlog

from app.core.config import settings

logger = structlog.get_logger()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token scheme
security = HTTPBearer()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)


def create_access_token(
    subject: Union[str, Any], 
    expires_delta: Optional[timedelta] = None,
    additional_claims: Optional[dict] = None
) -> str:
    """
    Create a JWT access token
    
    Args:
        subject: Token subject (usually user ID or email)
        expires_delta: Token expiration time
        additional_claims: Additional claims to include in token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "iat": datetime.utcnow(),
        "type": "access_token"
    }
    
    # Add additional claims if provided
    if additional_claims:
        to_encode.update(additional_claims)
    
    try:
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.SECRET_KEY, 
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error("Failed to create access token", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create access token"
        )


def create_refresh_token(subject: Union[str, Any]) -> str:
    """Create a JWT refresh token"""
    expire = datetime.utcnow() + timedelta(days=7)  # Refresh tokens last 7 days
    
    to_encode = {
        "exp": expire,
        "sub": str(subject),
        "iat": datetime.utcnow(),
        "type": "refresh_token"
    }
    
    try:
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt
    except Exception as e:
        logger.error("Failed to create refresh token", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Could not create refresh token"
        )


def verify_token(token: str) -> Optional[dict]:
    """
    Verify and decode a JWT token
    
    Returns:
        Token payload if valid, None if invalid
    """
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError as e:
        logger.warning("Token verification failed", error=str(e))
        return None
    except Exception as e:
        logger.error("Unexpected error verifying token", error=str(e))
        return None


async def get_current_user_from_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """
    Get current user from JWT token
    
    Returns:
        User information from token payload
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = verify_token(credentials.credentials)
        if payload is None:
            raise credentials_exception
            
        # Check token type
        token_type = payload.get("type")
        if token_type != "access_token":
            logger.warning("Invalid token type", token_type=token_type)
            raise credentials_exception
            
        # Get user identifier
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
            
        return {
            "user_id": user_id,
            "email": payload.get("email"),
            "username": payload.get("username"),
            "is_superuser": payload.get("is_superuser", False),
            "organization_id": payload.get("organization_id"),
            "permissions": payload.get("permissions", [])
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error getting current user", error=str(e))
        raise credentials_exception


def generate_api_key() -> str:
    """Generate a secure API key"""
    return secrets.token_urlsafe(32)


def verify_api_key(api_key: str) -> bool:
    """
    Verify an API key (placeholder implementation)
    In production, this would check against a database
    """
    # This is a placeholder - in production you'd check against a database
    valid_api_keys = [
        "demo-api-key-12345",
        "test-api-key-67890"
    ]
    return api_key in valid_api_keys


async def get_api_key(request: Request) -> Optional[str]:
    """Extract API key from request headers"""
    api_key = request.headers.get("X-API-Key")
    if not api_key:
        api_key = request.headers.get("Authorization")
        if api_key and api_key.startswith("Bearer "):
            api_key = api_key[7:]  # Remove "Bearer " prefix
    return api_key


class RateLimiter:
    """Simple rate limiting implementation"""
    
    def __init__(self):
        self.requests = {}
    
    def is_allowed(self, identifier: str, limit: int = 100, window: int = 900) -> bool:
        """
        Check if request is allowed based on rate limit
        
        Args:
            identifier: Unique identifier (IP, user ID, etc.)
            limit: Maximum requests per window
            window: Time window in seconds
        """
        now = datetime.utcnow().timestamp()
        
        if identifier not in self.requests:
            self.requests[identifier] = []
        
        # Clean old requests
        self.requests[identifier] = [
            req_time for req_time in self.requests[identifier]
            if now - req_time < window
        ]
        
        # Check limit
        if len(self.requests[identifier]) >= limit:
            return False
        
        # Add current request
        self.requests[identifier].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


async def check_rate_limit(request: Request) -> bool:
    """Rate limiting dependency"""
    client_ip = request.client.host if request.client else "unknown"
    
    if not rate_limiter.is_allowed(
        client_ip, 
        settings.RATE_LIMIT_REQUESTS, 
        settings.RATE_LIMIT_WINDOW
    ):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    return True


def require_permissions(required_permissions: list):
    """
    Decorator to require specific permissions
    
    Args:
        required_permissions: List of required permission strings
    """
    def permission_checker(current_user: dict = Depends(get_current_user_from_token)):
        user_permissions = current_user.get("permissions", [])
        
        # Superusers have all permissions
        if current_user.get("is_superuser", False):
            return current_user
        
        # Check if user has required permissions
        if not all(perm in user_permissions for perm in required_permissions):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        
        return current_user
    
    return permission_checker


def require_superuser(current_user: dict = Depends(get_current_user_from_token)):
    """Require superuser access"""
    if not current_user.get("is_superuser", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Superuser access required"
        )
    return current_user


class SecurityHeaders:
    """Security headers middleware utilities"""
    
    @staticmethod
    def get_security_headers() -> dict:
        """Get standard security headers"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Referrer-Policy": "strict-origin-when-cross-origin",
            "Content-Security-Policy": "default-src 'self'",
        }


def validate_password_strength(password: str) -> bool:
    """
    Validate password strength
    
    Requirements:
    - At least 8 characters
    - Contains uppercase and lowercase letters
    - Contains at least one digit
    - Contains at least one special character
    """
    if len(password) < 8:
        return False
    
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    return all([has_upper, has_lower, has_digit, has_special])


def generate_password_reset_token(email: str) -> str:
    """Generate a password reset token"""
    expire = datetime.utcnow() + timedelta(hours=1)  # Reset tokens expire in 1 hour
    
    to_encode = {
        "exp": expire,
        "sub": email,
        "iat": datetime.utcnow(),
        "type": "password_reset"
    }
    
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )


def verify_password_reset_token(token: str) -> Optional[str]:
    """Verify password reset token and return email"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        if payload.get("type") != "password_reset":
            return None
            
        return payload.get("sub")
    except JWTError:
        return None


# OAuth2 scheme for documentation
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    scheme_name="JWT"
) 