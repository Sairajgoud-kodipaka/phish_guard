"""
PhishGuard Backend Logging Configuration
Structured logging setup using structlog
"""

import logging
import sys
import structlog
from typing import Any
import json
from datetime import datetime

from app.core.config import settings


def setup_logging():
    """Configure structured logging for the application"""
    
    # Configure standard library logging
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        format="%(message)s",
        stream=sys.stdout
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            # Add timestamp
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            add_timestamp,
            add_correlation_id,
            # JSON formatting for production, pretty printing for development
            structlog.dev.ConsoleRenderer() if settings.is_development 
            else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def add_timestamp(logger, method_name, event_dict):
    """Add timestamp to log entries"""
    event_dict["timestamp"] = datetime.utcnow().isoformat() + "Z"
    return event_dict


def add_correlation_id(logger, method_name, event_dict):
    """Add correlation ID to log entries (for request tracing)"""
    # In a real implementation, this would extract correlation ID from context
    # For now, we'll just add a placeholder
    event_dict["correlation_id"] = getattr(logger, "_correlation_id", None)
    return event_dict


class SecurityLogger:
    """Security-focused logging utilities"""
    
    def __init__(self):
        self.logger = structlog.get_logger("security")
    
    def log_auth_attempt(self, email: str, success: bool, ip_address: str = None):
        """Log authentication attempts"""
        self.logger.info(
            "Authentication attempt",
            email=email,
            success=success,
            ip_address=ip_address,
            event_type="auth_attempt"
        )
    
    def log_permission_denied(self, user_id: str, resource: str, action: str):
        """Log permission denied events"""
        self.logger.warning(
            "Permission denied",
            user_id=user_id,
            resource=resource,
            action=action,
            event_type="permission_denied"
        )
    
    def log_suspicious_activity(self, user_id: str, activity: str, details: dict = None):
        """Log suspicious activities"""
        self.logger.warning(
            "Suspicious activity detected",
            user_id=user_id,
            activity=activity,
            details=details or {},
            event_type="suspicious_activity"
        )
    
    def log_data_access(self, user_id: str, resource: str, action: str, sensitive: bool = False):
        """Log data access events"""
        log_level = "warning" if sensitive else "info"
        getattr(self.logger, log_level)(
            "Data access",
            user_id=user_id,
            resource=resource,
            action=action,
            sensitive=sensitive,
            event_type="data_access"
        )


class ThreatLogger:
    """Threat detection logging utilities"""
    
    def __init__(self):
        self.logger = structlog.get_logger("threat_detection")
    
    def log_threat_detected(self, email_id: str, threat_type: str, confidence: float, details: dict = None):
        """Log threat detection events"""
        self.logger.warning(
            "Threat detected",
            email_id=email_id,
            threat_type=threat_type,
            confidence=confidence,
            details=details or {},
            event_type="threat_detected"
        )
    
    def log_false_positive(self, email_id: str, original_threat: str, corrected_by: str):
        """Log false positive corrections"""
        self.logger.info(
            "False positive reported",
            email_id=email_id,
            original_threat=original_threat,
            corrected_by=corrected_by,
            event_type="false_positive"
        )
    
    def log_analysis_error(self, email_id: str, error_type: str, error_message: str):
        """Log analysis errors"""
        self.logger.error(
            "Analysis error",
            email_id=email_id,
            error_type=error_type,
            error_message=error_message,
            event_type="analysis_error"
        )


class PerformanceLogger:
    """Performance monitoring logging utilities"""
    
    def __init__(self):
        self.logger = structlog.get_logger("performance")
    
    def log_request_timing(self, endpoint: str, method: str, duration: float, status_code: int):
        """Log API request timing"""
        self.logger.info(
            "Request completed",
            endpoint=endpoint,
            method=method,
            duration_ms=round(duration * 1000, 2),
            status_code=status_code,
            event_type="request_timing"
        )
    
    def log_db_query_timing(self, query_type: str, duration: float, rows_affected: int = None):
        """Log database query timing"""
        self.logger.info(
            "Database query",
            query_type=query_type,
            duration_ms=round(duration * 1000, 2),
            rows_affected=rows_affected,
            event_type="db_query"
        )
    
    def log_ml_processing_timing(self, email_id: str, model_name: str, duration: float):
        """Log ML processing timing"""
        self.logger.info(
            "ML processing completed",
            email_id=email_id,
            model_name=model_name,
            duration_ms=round(duration * 1000, 2),
            event_type="ml_processing"
        )


class AuditLogger:
    """Audit trail logging utilities"""
    
    def __init__(self):
        self.logger = structlog.get_logger("audit")
    
    def log_user_action(self, user_id: str, action: str, resource: str, old_value: Any = None, new_value: Any = None):
        """Log user actions for audit trail"""
        self.logger.info(
            "User action",
            user_id=user_id,
            action=action,
            resource=resource,
            old_value=self._sanitize_value(old_value),
            new_value=self._sanitize_value(new_value),
            event_type="user_action"
        )
    
    def log_system_event(self, event: str, details: dict = None):
        """Log system events"""
        self.logger.info(
            "System event",
            event=event,
            details=details or {},
            event_type="system_event"
        )
    
    def log_configuration_change(self, user_id: str, setting: str, old_value: Any, new_value: Any):
        """Log configuration changes"""
        self.logger.warning(
            "Configuration changed",
            user_id=user_id,
            setting=setting,
            old_value=self._sanitize_value(old_value),
            new_value=self._sanitize_value(new_value),
            event_type="config_change"
        )
    
    def _sanitize_value(self, value: Any) -> str:
        """Sanitize values for logging (remove sensitive data)"""
        if value is None:
            return None
        
        # Convert to string and truncate if too long
        str_value = str(value)
        if len(str_value) > 1000:
            str_value = str_value[:1000] + "... (truncated)"
        
        # Remove potential sensitive patterns
        sensitive_patterns = ["password", "token", "key", "secret"]
        for pattern in sensitive_patterns:
            if pattern in str_value.lower():
                return "[REDACTED]"
        
        return str_value


# Global logger instances
security_logger = SecurityLogger()
threat_logger = ThreatLogger()
performance_logger = PerformanceLogger()
audit_logger = AuditLogger()


def get_logger(name: str = None) -> structlog.BoundLogger:
    """Get a structured logger instance"""
    return structlog.get_logger(name)


class LoggingMiddleware:
    """Custom logging middleware for FastAPI"""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger("middleware")
    
    async def __call__(self, scope, receive, send):
        """Process requests with logging"""
        if scope["type"] == "http":
            # Log request start
            self.logger.info(
                "Request started",
                method=scope["method"],
                path=scope["path"],
                query_string=scope.get("query_string", b"").decode(),
            )
        
        await self.app(scope, receive, send)


# Utility functions for common logging patterns
def log_exception(logger: structlog.BoundLogger, exc: Exception, context: dict = None):
    """Log exceptions with context"""
    logger.error(
        "Exception occurred",
        exception_type=type(exc).__name__,
        exception_message=str(exc),
        context=context or {},
        exc_info=True
    )


def log_metrics(metric_name: str, value: float, tags: dict = None):
    """Log metrics for monitoring systems"""
    metrics_logger = get_logger("metrics")
    metrics_logger.info(
        "Metric recorded",
        metric_name=metric_name,
        value=value,
        tags=tags or {},
        event_type="metric"
    )


# Context manager for request correlation
class RequestContext:
    """Context manager for request correlation IDs"""
    
    def __init__(self, correlation_id: str):
        self.correlation_id = correlation_id
        self.logger = get_logger()
    
    def __enter__(self):
        self.logger._correlation_id = self.correlation_id
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self.logger, '_correlation_id'):
            delattr(self.logger, '_correlation_id') 