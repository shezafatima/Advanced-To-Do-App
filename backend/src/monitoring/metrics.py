"""
Metrics and monitoring for the Todo Full-Stack Web Application.

This module provides application metrics collection and monitoring capabilities.
"""

from datetime import datetime
from typing import Dict, Any, Optional
from enum import Enum

from ..logging.utils import log_performance_metric
from ..logging.logger_config import get_logger


class MetricType(Enum):
    """Types of metrics that can be tracked."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    SUMMARY = "summary"


class MetricsCollector:
    """Centralized metrics collector for application monitoring."""

    def __init__(self):
        self.metrics: Dict[str, Dict[str, Any]] = {}
        self.logger = get_logger("metrics")

    def increment_counter(self, name: str, labels: Optional[Dict[str, str]] = None, value: int = 1):
        """Increment a counter metric."""
        metric_key = self._get_metric_key(name, labels)

        if metric_key not in self.metrics:
            self.metrics[metric_key] = {
                "type": MetricType.COUNTER,
                "value": 0,
                "labels": labels or {},
                "created_at": datetime.utcnow()
            }

        self.metrics[metric_key]["value"] += value

        # Log performance metric
        log_performance_metric(
            name,
            self.metrics[metric_key]["value"],
            logger_name="metrics"
        )

    def set_gauge(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Set a gauge metric to a specific value."""
        metric_key = self._get_metric_key(name, labels)

        self.metrics[metric_key] = {
            "type": MetricType.GAUGE,
            "value": value,
            "labels": labels or {},
            "updated_at": datetime.utcnow()
        }

        # Log performance metric
        log_performance_metric(
            name,
            value,
            logger_name="metrics"
        )

    def observe_histogram(self, name: str, value: float, labels: Optional[Dict[str, str]] = None):
        """Observe a value in a histogram metric."""
        metric_key = self._get_metric_key(name, labels)

        if metric_key not in self.metrics:
            self.metrics[metric_key] = {
                "type": MetricType.HISTOGRAM,
                "values": [],
                "labels": labels or {},
                "created_at": datetime.utcnow()
            }

        self.metrics[metric_key]["values"].append(value)

        # Log performance metric
        log_performance_metric(
            name,
            value,
            logger_name="metrics"
        )

    def get_metric(self, name: str, labels: Optional[Dict[str, str]] = None) -> Optional[Dict[str, Any]]:
        """Get a specific metric by name and labels."""
        metric_key = self._get_metric_key(name, labels)
        return self.metrics.get(metric_key)

    def get_all_metrics(self) -> Dict[str, Dict[str, Any]]:
        """Get all collected metrics."""
        return self.metrics.copy()

    def _get_metric_key(self, name: str, labels: Optional[Dict[str, str]]) -> str:
        """Generate a unique key for a metric based on name and labels."""
        if not labels:
            return name

        # Sort labels to ensure consistent ordering
        sorted_labels = sorted(labels.items())
        labels_str = ",".join([f"{k}={v}" for k, v in sorted_labels])
        return f"{name}{{{labels_str}}}"

    def export_prometheus_format(self) -> str:
        """Export metrics in Prometheus text format."""
        lines = []

        for metric_key, metric_data in self.metrics.items():
            metric_type = metric_data["type"]
            labels = metric_data.get("labels", {})

            # Add TYPE comment
            lines.append(f"# TYPE {metric_type.value}_{metric_key.replace('{', '_').replace('}', '').replace(',', '_').replace('=', '_')}")

            if metric_type == MetricType.COUNTER:
                value = metric_data["value"]
                labels_str = self._format_labels(labels)
                lines.append(f"{metric_type.value}_{metric_key.split('{')[0]}{labels_str} {value}")

            elif metric_type == MetricType.GAUGE:
                value = metric_data["value"]
                labels_str = self._format_labels(labels)
                lines.append(f"{metric_type.value}_{metric_key.split('{')[0]}{labels_str} {value}")

            elif metric_type == MetricType.HISTOGRAM:
                values = metric_data["values"]
                if values:
                    # Add count and sum
                    count = len(values)
                    total = sum(values)

                    # Add count
                    labels_str = self._format_labels(labels)
                    lines.append(f"{metric_type.value}_{metric_key.split('{')[0]}_count{labels_str} {count}")

                    # Add sum
                    lines.append(f"{metric_type.value}_{metric_key.split('{')[0]}_sum{labels_str} {total}")

                    # Add buckets (simplified)
                    for i, val in enumerate(sorted(values)):
                        bucket_labels = {**labels, "le": str(val)}
                        bucket_labels_str = self._format_labels(bucket_labels)
                        lines.append(f"{metric_type.value}_{metric_key.split('{')[0]}_bucket{bucket_labels_str} {i+1}")

        return "\n".join(lines)

    def _format_labels(self, labels: Dict[str, str]) -> str:
        """Format labels for Prometheus output."""
        if not labels:
            return ""

        labels_str = ",".join([f'{k}="{v}"' for k, v in labels.items()])
        return f"{{{labels_str}}}"


# Global metrics collector instance
metrics_collector = MetricsCollector()


def track_api_request(method: str, path: str, status_code: int, duration_ms: float):
    """Track API request metrics."""
    # Count total requests
    metrics_collector.increment_counter(
        "api_requests_total",
        labels={"method": method, "path": path, "status_code": str(status_code)}
    )

    # Track request duration
    metrics_collector.observe_histogram(
        "api_request_duration_seconds",
        duration_ms / 1000.0,  # Convert to seconds
        labels={"method": method, "path": path}
    )


def track_user_action(action: str, user_id: str):
    """Track user action metrics."""
    metrics_collector.increment_counter(
        "user_actions_total",
        labels={"action": action, "user_id": user_id}
    )


def track_database_operation(operation: str, duration_ms: float, success: bool = True):
    """Track database operation metrics."""
    metrics_collector.increment_counter(
        "database_operations_total",
        labels={"operation": operation, "success": str(success)}
    )

    metrics_collector.observe_histogram(
        "database_operation_duration_seconds",
        duration_ms / 1000.0,  # Convert to seconds
        labels={"operation": operation}
    )


def track_todo_operation(operation: str, user_id: str):
    """Track todo-related operation metrics."""
    metrics_collector.increment_counter(
        "todo_operations_total",
        labels={"operation": operation, "user_id": user_id}
    )


def get_application_health_status() -> Dict[str, Any]:
    """Get overall application health status."""
    # In a real application, this would check database connectivity,
    # external service availability, etc.
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "metrics_count": len(metrics_collector.get_all_metrics()),
        "checks": {
            "database": "connected",
            "cache": "available",
            "external_apis": "reachable"
        }
    }


def initialize_monitoring():
    """Initialize monitoring system."""
    logger = get_logger("monitoring")
    logger.info("Monitoring system initialized")

    # Set initial gauge values
    metrics_collector.set_gauge("application_startup_time", datetime.utcnow().timestamp())

    # Log initialization
    logger.info("Metrics collector ready with initial application metrics")


# Initialize monitoring when module is imported
initialize_monitoring()