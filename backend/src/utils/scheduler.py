"""
Scheduler for handling recurring tasks and other periodic operations.
"""
import asyncio
import logging
from datetime import datetime
from sqlmodel import Session
from ..database.session import get_session_context
from ..services.todo_service import TodoService
import contextlib

logger = logging.getLogger(__name__)

class RecurringTaskScheduler:
    """
    Scheduler for processing recurring tasks and creating new instances.
    """

    def __init__(self):
        self.is_running = False

    async def start(self):
        """Start the recurring task processor."""
        if self.is_running:
            logger.warning("Scheduler is already running")
            return

        self.is_running = True
        logger.info("Starting recurring task scheduler...")

        while self.is_running:
            try:
                await self.process_recurring_tasks()
                # Wait for 1 hour before next check
                await asyncio.sleep(3600)
            except Exception as e:
                logger.error(f"Error in recurring task scheduler: {e}")
                # Wait for 5 minutes before retrying
                await asyncio.sleep(300)

    async def stop(self):
        """Stop the recurring task processor."""
        self.is_running = False
        logger.info("Stopping recurring task scheduler...")

    async def process_recurring_tasks(self):
        """Process all recurring tasks and create new instances as needed."""
        try:
            # Use the session context manager to handle database connections properly
            with get_session_context() as session:
                new_tasks_count = TodoService.process_recurring_tasks(session=session)
                if new_tasks_count > 0:
                    logger.info(f"Created {new_tasks_count} new recurring task instances")
                else:
                    logger.debug("No new recurring tasks created")
        except Exception as e:
            logger.error(f"Error processing recurring tasks: {e}")
            raise

# Global scheduler instance
scheduler = RecurringTaskScheduler()

def get_scheduler():
    """Get the global scheduler instance."""
    return scheduler