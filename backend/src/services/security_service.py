import logging
from datetime import datetime
from typing import Optional
from sqlmodel import Session
from ..models.user import User


class SecurityService:
    """
    Service class for handling security-related operations and audit trails.
    """

    # Configure logger
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Create handler
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)

    # Add handler to logger
    if not logger.handlers:
        logger.addHandler(handler)

    @staticmethod
    def log_user_action(user_id: str, action: str, resource: Optional[str] = None, details: Optional[str] = None):
        """
        Log a user action for audit trail purposes.
        """
        log_message = f"User {user_id} performed action '{action}'"
        if resource:
            log_message += f" on resource '{resource}'"
        if details:
            log_message += f" - Details: {details}"

        SecurityService.logger.info(log_message)

    @staticmethod
    def log_security_event(event_type: str, user_id: Optional[str] = None, ip_address: Optional[str] = None, details: Optional[str] = None):
        """
        Log a security-related event.
        """
        log_message = f"Security event: {event_type}"
        if user_id:
            log_message += f" by user {user_id}"
        if ip_address:
            log_message += f" from IP {ip_address}"
        if details:
            log_message += f" - Details: {details}"

        SecurityService.logger.warning(log_message)

    @staticmethod
    def validate_user_access(current_user: User, target_user_id: str) -> bool:
        """
        Validate that the current user has access to the target resource.
        For user-specific resources, this ensures the current user is the owner.
        """
        return str(current_user.id) == str(target_user_id)

    @staticmethod
    def validate_todo_access(current_user: User, todo_user_id: str) -> bool:
        """
        Validate that the current user has access to the specified todo.
        """
        return str(current_user.id) == str(todo_user_id)