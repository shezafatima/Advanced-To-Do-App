"""
Logging utilities for the Todo Full-Stack Web Application.

This module provides utility functions for structured logging,
performance monitoring, and error tracking throughout the application.
"""

import functools
import time
from typing import Callable, Optional

from .logger_config import get_logger, log_api_request, log_security_event, log_error_trace


def log_function_call(logger_name: str = "app"):
    """
    Decorator to log function calls with execution time and parameters.

    Args:
        logger_name: Name of the logger to use
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name)
            start_time = time.time()

            # Log function start
            args_str = ", ".join([repr(arg) for arg in args])
            kwargs_str = ", ".join([f"{k}={repr(v)}" for k, v in kwargs.items()])
            all_args = ", ".join(filter(None, [args_str, kwargs_str]))

            logger.debug(f"Calling {func.__name__}({all_args})")

            try:
                result = func(*args, **kwargs)
                execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
                logger.debug(
                    f"{func.__name__} completed in {execution_time:.2f}ms"
                )
                return result
            except Exception as e:
                execution_time = (time.time() - start_time) * 1000
                logger.error(
                    f"{func.__name__} failed after {execution_time:.2f}ms: {str(e)}"
                )
                raise

        return wrapper
    return decorator


def log_execution_time(logger_name: str = "app"):
    """
    Decorator to measure and log execution time of functions.

    Args:
        logger_name: Name of the logger to use
    """
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            logger = get_logger(logger_name)
            start_time = time.time()

            result = func(*args, **kwargs)

            execution_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            logger.info(f"{func.__name__} executed in {execution_time:.2f}ms")

            return result
        return wrapper
    return decorator


def log_user_action(
    action: str,
    user_id: Optional[str] = None,
    details: Optional[dict] = None,
    logger_name: str = "app"
):
    """
    Log user actions for audit trail and analytics.

    Args:
        action: Description of the action taken
        user_id: ID of the user performing the action
        details: Additional details about the action
        logger_name: Name of the logger to use
    """
    logger = get_logger(logger_name)

    user_info = f" (user: {user_id})" if user_id else " (anonymous)"
    details_str = f" - Details: {details}" if details else ""

    logger.info(f"USER ACTION: {action}{user_info}{details_str}")


def log_performance_metric(
    metric_name: str,
    value: float,
    unit: str = "",
    logger_name: str = "app"
):
    """
    Log performance metrics for monitoring.

    Args:
        metric_name: Name of the metric
        value: Metric value
        unit: Unit of measurement
        logger_name: Name of the logger to use
    """
    logger = get_logger(logger_name)
    unit_str = f" {unit}" if unit else ""
    logger.info(f"PERFORMANCE METRIC: {metric_name} = {value}{unit_str}")


def log_database_query(
    query: str,
    execution_time: float,
    rows_affected: Optional[int] = None,
    logger_name: str = "database"
):
    """
    Log database query execution details.

    Args:
        query: SQL query executed
        execution_time: Time taken to execute the query in milliseconds
        rows_affected: Number of rows affected by the query (for INSERT/UPDATE/DELETE)
        logger_name: Name of the logger to use
    """
    logger = get_logger(logger_name)

    rows_str = f" ({rows_affected} rows)" if rows_affected is not None else ""
    logger.debug(f"DB QUERY: {query[:100]}...{rows_str} took {execution_time:.2f}ms")


def log_cache_operation(
    operation: str,
    key: str,
    hit: bool = None,
    logger_name: str = "app"
):
    """
    Log cache operations for performance monitoring.

    Args:
        operation: Type of operation (get, set, delete)
        key: Cache key involved
        hit: Whether it was a cache hit (for get operations)
        logger_name: Name of the logger to use
    """
    logger = get_logger(logger_name)

    hit_str = f" (hit: {hit})" if hit is not None else ""
    logger.debug(f"CACHE {operation.upper()}: {key}{hit_str}")