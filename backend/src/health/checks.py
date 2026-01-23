from typing import Dict, Any
from sqlmodel import select
from ..database.session import engine
from ..models.user import User
import time


class HealthChecker:
    """
    Class to perform various health checks on the application.
    """

    @staticmethod
    def check_database_connection() -> Dict[str, Any]:
        """
        Check if the database connection is healthy.

        Returns:
            Dictionary with status information
        """
        try:
            # Try to execute a simple query
            with engine.connect() as conn:
                # Execute a simple query to test the connection
                result = conn.execute(select(User).limit(1)).fetchone()

            return {
                "status": "healthy",
                "message": "Database connection is healthy",
                "response_time_ms": 0  # Placeholder, in real implementation measure actual time
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Database connection failed: {str(e)}",
                "error": str(e)
            }

    @staticmethod
    def check_database_performance() -> Dict[str, Any]:
        """
        Check database performance by measuring query execution time.

        Returns:
            Dictionary with performance information
        """
        start_time = time.time()

        try:
            # Execute a simple query to measure response time
            with engine.connect() as conn:
                conn.execute(select(User).limit(1)).fetchone()

            response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

            # Consider slow queries as performance issues
            if response_time > 1000:  # More than 1 second
                status = "degraded"
                message = f"Database response time is high: {response_time:.2f}ms"
            else:
                status = "healthy"
                message = f"Database response time is acceptable: {response_time:.2f}ms"

            return {
                "status": status,
                "message": message,
                "response_time_ms": round(response_time, 2)
            }
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Database performance check failed: {str(e)}",
                "error": str(e),
                "response_time_ms": -1
            }

    @staticmethod
    def check_application_health() -> Dict[str, Any]:
        """
        Check overall application health.

        Returns:
            Dictionary with application health information
        """
        db_check = HealthChecker.check_database_connection()

        if db_check["status"] == "healthy":
            return {
                "status": "healthy",
                "message": "Application is healthy",
                "checks": {
                    "database": db_check
                }
            }
        else:
            return {
                "status": "unhealthy",
                "message": "Application is unhealthy",
                "checks": {
                    "database": db_check
                }
            }

    @staticmethod
    def get_detailed_health_report() -> Dict[str, Any]:
        """
        Get a detailed health report including multiple checks.

        Returns:
            Dictionary with detailed health information
        """
        db_connection = HealthChecker.check_database_connection()
        db_performance = HealthChecker.check_database_performance()

        # Determine overall status
        if db_connection["status"] == "unhealthy":
            overall_status = "unhealthy"
        elif db_connection["status"] == "degraded" or db_performance["status"] == "degraded":
            overall_status = "degraded"
        else:
            overall_status = "healthy"

        return {
            "status": overall_status,
            "timestamp": time.time(),
            "checks": {
                "database_connection": db_connection,
                "database_performance": db_performance
            }
        }