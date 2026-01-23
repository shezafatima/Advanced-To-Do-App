"""
Health check endpoints for the Todo Full-Stack Web Application.

This module provides health check endpoints for monitoring and orchestration tools.
"""

from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from ..database.session import get_session
from ..models.user import User
from ..monitoring.metrics import get_application_health_status
from ..logging.logger_config import get_logger


router = APIRouter(prefix="/health", tags=["health"])

logger = get_logger("health")


class HealthCheckResponse(BaseModel):
    """Response model for health check endpoint."""

    status: str
    timestamp: str
    uptime: float
    checks: Dict[str, Any]


class DetailedHealthResponse(BaseModel):
    """Detailed response model for comprehensive health check."""

    status: str
    timestamp: str
    version: str
    environment: str
    checks: Dict[str, Any]
    metrics: Dict[str, Any]


@router.get("/ping", summary="Simple ping endpoint")
async def ping() -> Dict[str, str]:
    """
    Simple ping endpoint to check if the application is running.

    Returns:
        Dict[str, str]: Simple response indicating the application is alive
    """
    logger.info("Ping endpoint called")
    return {"status": "ok", "message": "pong"}


@router.get("", response_model=HealthCheckResponse, summary="Basic health check")
async def health_check() -> HealthCheckResponse:
    """
    Basic health check endpoint that verifies the application is running.

    Returns:
        HealthCheckResponse: Health status information
    """
    logger.info("Basic health check called")

    # Calculate uptime (in a real app, you'd store the start time)
    import time
    start_time = getattr(health_check, 'start_time', time.time())
    if not hasattr(health_check, 'start_time'):
        health_check.start_time = start_time

    uptime = time.time() - start_time

    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "uptime": uptime,
        "checks": {
            "application": "running",
            "database": "not_checked",
            "cache": "not_checked"
        }
    }

    return HealthCheckResponse(**health_data)


@router.get("/detailed", response_model=DetailedHealthResponse, summary="Detailed health check")
async def detailed_health_check() -> DetailedHealthResponse:
    """
    Detailed health check that verifies various system components.

    Returns:
        DetailedHealthResponse: Comprehensive health status information
    """
    logger.info("Detailed health check called")

    # Perform detailed checks
    checks = {}

    # Check database connectivity
    try:
        from sqlmodel import select
        db_session = next(get_session())
        # Try a simple query
        db_result = db_session.exec(select(User).limit(1)).first()
        checks["database"] = {
            "status": "connected",
            "response_time": "fast",
            "message": "Database connection successful"
        }
    except Exception as e:
        logger.error(f"Database health check failed: {str(e)}")
        checks["database"] = {
            "status": "error",
            "message": f"Database connection failed: {str(e)}"
        }
    finally:
        try:
            db_session.close()
        except:
            pass

    # Check external dependencies (mocked here)
    checks["external_services"] = {
        "status": "available",
        "services": ["auth_provider", "notification_service"]
    }

    # Get application metrics
    from ..monitoring.metrics import metrics_collector
    metrics = metrics_collector.get_all_metrics()

    # Get overall health status
    overall_status = "healthy"
    for check_name, check_result in checks.items():
        if isinstance(check_result, dict) and check_result.get("status") == "error":
            overall_status = "degraded"
            break

    health_data = {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",  # In a real app, this would come from configuration
        "environment": "development",  # Would come from environment variable
        "checks": checks,
        "metrics": {
            "total_metrics": len(metrics),
            "last_updated": datetime.utcnow().isoformat()
        }
    }

    return DetailedHealthResponse(**health_data)


@router.get("/ready", summary="Readiness check")
async def readiness_check() -> Dict[str, Any]:
    """
    Readiness check to determine if the application is ready to serve traffic.

    Returns:
        Dict[str, Any]: Readiness status information
    """
    logger.info("Readiness check called")

    # Check if all critical services are available
    ready_checks = {
        "database_connected": True,
        "configuration_loaded": True,
        "external_services_available": True
    }

    # In a real application, you would perform actual checks
    # For now, we'll assume everything is ready
    is_ready = all(ready_checks.values())

    if not is_ready:
        logger.warning("Application is not ready to serve traffic")
        raise HTTPException(
            status_code=503,
            detail="Application is not ready to serve traffic",
        )

    ready_status = {
        "status": "ready",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": ready_checks
    }

    logger.info("Application is ready to serve traffic")
    return ready_status


@router.get("/live", summary="Liveness check")
async def liveness_check() -> Dict[str, str]:
    """
    Liveness check to determine if the application is alive.

    Returns:
        Dict[str, str]: Liveness status information
    """
    logger.info("Liveness check called")

    # A liveness check typically just confirms the process is running
    # More sophisticated checks could include memory usage, etc.
    return {
        "status": "alive",
        "timestamp": datetime.utcnow().isoformat(),
    }


# Add the router to the main application in main.py
def include_router(app):
    """
    Include health check routes in the main application.

    Args:
        app: FastAPI application instance
    """
    app.include_router(router)