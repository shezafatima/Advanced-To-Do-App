from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.rrule import rrule, DAILY, WEEKLY, MONTHLY, YEARLY
from ..models.todo import Todo, TodoCreate, TodoUpdate, TodoToggle, TodoAdvancedRead
from ..models.tag import Tag, TagCreate
from ..models.user import User
from ..utils.errors import TodoNotFoundException, UnauthorizedAccessException, TagNotFoundException


class TodoService:
    """
    Service class for handling advanced todo-related operations.
    """

    @staticmethod
    def create_todo(*, session: Session, todo_create: TodoCreate, user_id: UUID) -> Todo:
        """
        Create a new todo for the specified user with advanced features.
        """
        todo = Todo(
            title=todo_create.title,
            description=todo_create.description,
            completed=todo_create.completed if hasattr(todo_create, 'completed') else False,
            user_id=user_id,
            priority=todo_create.priority if hasattr(todo_create, 'priority') and todo_create.priority is not None else Todo.__fields__['priority'].default,
            due_date=todo_create.due_date,
            recurrence_rule=todo_create.recurrence_rule
        )

        session.add(todo)
        session.commit()
        session.refresh(todo)

        return todo

    @staticmethod
    def get_todo_by_id(*, session: Session, todo_id: UUID, user_id: UUID) -> Optional[Todo]:
        """
        Get a todo by its ID, ensuring it belongs to the specified user.
        """
        todo = session.get(Todo, todo_id)

        if not todo:
            return None

        # Verify that the todo belongs to the user
        if str(todo.user_id) != str(user_id):
            raise UnauthorizedAccessException()

        return todo

    @staticmethod
    def get_todos_for_user(*, session: Session, user_id: UUID) -> List[Todo]:
        """
        Get all todos for the specified user.
        """
        todos = session.exec(
            select(Todo).where(Todo.user_id == user_id)
        ).all()

        return todos

    @staticmethod
    def get_advanced_todos_for_user(*, session: Session, user_id: UUID) -> List[TodoAdvancedRead]:
        """
        Get all todos for the specified user with advanced features and tags.
        """
        todos = session.exec(
            select(Todo).where(Todo.user_id == user_id)
        ).all()

        # For now, returning basic todo data without tags (will implement tag joins later)
        result = []
        for todo in todos:
            todo_dict = todo.dict()
            # Add empty tags list for now
            todo_dict['tags'] = []
            result.append(TodoAdvancedRead(**todo_dict))

        return result

    @staticmethod
    def update_todo(*, session: Session, todo_id: UUID, todo_update: TodoUpdate, user_id: UUID) -> Optional[Todo]:
        """
        Update a todo, ensuring it belongs to the specified user.
        For recurring tasks, updates only future occurrences.
        """
        todo = session.get(Todo, todo_id)

        if not todo:
            raise TodoNotFoundException(str(todo_id))

        # Verify that the todo belongs to the user
        if str(todo.user_id) != str(user_id):
            raise UnauthorizedAccessException()

        # Check if this is a recurring task
        is_recurring = todo.recurrence_rule is not None and todo.recurrence_rule.strip() != ""

        # For recurring tasks, we need to handle updates differently
        if is_recurring:
            # For recurring tasks, only update the master template
            # The changes will apply to future occurrences when they are generated
            if todo_update.title is not None:
                todo.title = todo_update.title
            if todo_update.description is not None:
                todo.description = todo_update.description
            if todo_update.completed is not None:
                # For recurring tasks, we typically don't mark the template as completed
                # Instead, we generate new instances. But if explicitly set, we respect it.
                todo.completed = todo_update.completed
            if todo_update.priority is not None:
                todo.priority = todo_update.priority
            if todo_update.due_date is not None:
                # Update the due date for the template - this affects future occurrences
                todo.due_date = todo_update.due_date
            if todo_update.recurrence_rule is not None:
                # Update the recurrence rule - this affects future occurrences
                todo.recurrence_rule = todo_update.recurrence_rule
        else:
            # For non-recurring tasks, update all fields normally
            if todo_update.title is not None:
                todo.title = todo_update.title
            if todo_update.description is not None:
                todo.description = todo_update.description
            if todo_update.completed is not None:
                todo.completed = todo_update.completed
            if todo_update.priority is not None:
                todo.priority = todo_update.priority
            if todo_update.due_date is not None:
                todo.due_date = todo_update.due_date
            if todo_update.recurrence_rule is not None:
                todo.recurrence_rule = todo_update.recurrence_rule

        session.add(todo)
        session.commit()
        session.refresh(todo)

        return todo

    @staticmethod
    def delete_todo(*, session: Session, todo_id: UUID, user_id: UUID) -> bool:
        """
        Delete a todo, ensuring it belongs to the specified user.
        """
        todo = session.get(Todo, todo_id)

        if not todo:
            raise TodoNotFoundException(str(todo_id))

        # Verify that the todo belongs to the user
        if str(todo.user_id) != str(user_id):
            raise UnauthorizedAccessException()

        session.delete(todo)
        session.commit()

        return True

    @staticmethod
    def toggle_todo_completion(*, session: Session, todo_id: UUID, todo_toggle: TodoToggle, user_id: UUID) -> Optional[Todo]:
        """
        Toggle the completion status of a todo, ensuring it belongs to the specified user.
        """
        todo = session.get(Todo, todo_id)

        if not todo:
            raise TodoNotFoundException(str(todo_id))

        # Verify that the todo belongs to the user
        if str(todo.user_id) != str(user_id):
            raise UnauthorizedAccessException()

        # Update the completion status
        todo.completed = todo_toggle.completed

        session.add(todo)
        session.commit()
        session.refresh(todo)

        return todo

    @staticmethod
    def generate_recurring_tasks(*, session: Session, todo: Todo) -> List[Todo]:
        """
        Generate recurring task instances based on the recurrence rule.
        """
        if not todo.recurrence_rule:
            return []

        # Parse the recurrence rule (RRULE format)
        rule_parts = todo.recurrence_rule.split(';')
        freq_map = {
            'DAILY': DAILY,
            'WEEKLY': WEEKLY,
            'MONTHLY': MONTHLY,
            'YEARLY': YEARLY
        }

        freq = None
        interval = 1
        count = None
        until = None

        for part in rule_parts:
            if '=' in part:
                key, value = part.split('=', 1)
                if key == 'FREQ':
                    freq = freq_map.get(value)
                elif key == 'INTERVAL':
                    interval = int(value)
                elif key == 'COUNT':
                    count = int(value)
                elif key == 'UNTIL':
                    # Parse the UNTIL date in YYYYMMDDTHHMMSSZ format
                    try:
                        until = datetime.strptime(value, '%Y%m%dT%H%M%S%z')
                    except ValueError:
                        try:
                            until = datetime.strptime(value, '%Y%m%d')
                        except ValueError:
                            # If parsing fails, set a reasonable default
                            until = datetime.now() + timedelta(days=365)

        if not freq:
            return []

        # Generate the recurrence dates
        start_date = todo.created_at if todo.due_date is None else datetime.fromisoformat(todo.due_date.replace('Z', '+00:00'))

        # Create the rule
        rule = rrule.rrule(
            freq=freq,
            dtstart=start_date,
            interval=interval,
            count=count,
            until=until
        )

        # Generate new task instances for each occurrence (up to a reasonable limit)
        recurring_tasks = []
        max_instances = 100  # Limit to prevent infinite loops

        for i, occurrence in enumerate(rule):
            if i >= max_instances:
                break

            # Skip if this is the original task's occurrence
            if occurrence.date() == start_date.date():
                continue

            # Create a new task instance for this occurrence
            new_todo = Todo(
                title=todo.title,
                description=todo.description,
                completed=False,  # New recurring tasks start as incomplete
                user_id=todo.user_id,
                priority=todo.priority,
                due_date=occurrence.isoformat(),
                recurrence_rule=todo.recurrence_rule  # Preserve the rule for future generations
            )

            recurring_tasks.append(new_todo)

        return recurring_tasks

    @staticmethod
    def process_recurring_tasks(*, session: Session) -> int:
        """
        Process all recurring tasks and create new instances as needed.
        Returns the number of new tasks created.
        """
        # Get all recurring tasks
        recurring_todos = session.exec(
            select(Todo).where(Todo.recurrence_rule.is_not(None))
        ).all()

        new_tasks_created = 0

        for todo in recurring_todos:
            # Generate new task instances based on recurrence rule
            new_tasks = TodoService.generate_recurring_tasks(session=session, todo=todo)

            for new_task in new_tasks:
                # Check if a task for this date already exists to avoid duplicates
                existing_task = session.exec(
                    select(Todo).where(
                        Todo.title == new_task.title,
                        Todo.user_id == new_task.user_id,
                        Todo.due_date == new_task.due_date
                    )
                ).first()

                if not existing_task:
                    session.add(new_task)
                    new_tasks_created += 1

        session.commit()
        return new_tasks_created


class TagService:
    """
    Service class for handling tag-related operations.
    """

    @staticmethod
    def create_tag(*, session: Session, tag_create: TagCreate) -> Tag:
        """
        Create a new tag with auto-assigned color if not provided.
        """
        # Check if tag with same name already exists
        existing_tag = session.exec(
            select(Tag).where(Tag.name == tag_create.name)
        ).first()

        if existing_tag:
            return existing_tag  # Return existing tag to avoid duplicates

        # Auto-assign color if not provided
        color = tag_create.color
        if not color or color == "#default":
            color = TodoService._generate_auto_color(tag_create.name)

        tag = Tag(
            name=tag_create.name,
            color=color
        )

        session.add(tag)
        session.commit()
        session.refresh(tag)

        return tag

    @staticmethod
    def _generate_auto_color(tag_name: str) -> str:
        """
        Generate a consistent color based on the tag name for auto-assignment.
        """
        import hashlib

        # Create a hash of the tag name to generate a consistent color
        hash_object = hashlib.md5(tag_name.encode())
        hex_dig = hash_object.hexdigest()

        # Take the first 6 characters of the hash and make it a hex color
        color = f"#{hex_dig[:6]}"

        # Ensure it's a valid hex color by limiting to safe values if needed
        # Just in case the hash produces invalid hex, we'll return a default
        if len(color) != 7 or not all(c in '0123456789abcdefABCDEF' for c in color[1:]):
            # Generate a random color based on the hash
            r = int(hex_dig[:2], 16) % 256
            g = int(hex_dig[2:4], 16) % 256
            b = int(hex_dig[4:6], 16) % 256
            color = f"#{r:02x}{g:02x}{b:02x}"

        return color

    @staticmethod
    def get_tag_by_id(*, session: Session, tag_id: UUID) -> Optional[Tag]:
        """
        Get a tag by its ID.
        """
        tag = session.get(Tag, tag_id)
        return tag

    @staticmethod
    def get_tag_by_name(*, session: Session, name: str) -> Optional[Tag]:
        """
        Get a tag by its name.
        """
        tag = session.exec(
            select(Tag).where(Tag.name == name)
        ).first()
        return tag

    @staticmethod
    def get_all_tags(*, session: Session) -> List[Tag]:
        """
        Get all tags.
        """
        tags = session.exec(select(Tag)).all()
        return tags


class UserProfileService:
    """
    Service class for handling user profile-related operations.
    """

    @staticmethod
    def create_profile(*, session: Session, user_id: UUID, display_name: str,
                      preferred_language: str = "en", theme_preference: Optional[str] = None,
                      notification_preferences: Optional[dict] = None) -> 'UserProfile':
        from ..models.profile import UserProfile
        import json

        if notification_preferences is None:
            notification_preferences = {"toast_notifications": True}

        profile = UserProfile(
            user_id=user_id,
            display_name=display_name,
            preferred_language=preferred_language,
            theme_preference=theme_preference,
            notification_preferences=json.dumps(notification_preferences)
        )

        session.add(profile)
        session.commit()
        session.refresh(profile)

        return profile

    @staticmethod
    def get_profile_by_user_id(*, session: Session, user_id: UUID) -> Optional['UserProfile']:
        from ..models.profile import UserProfile
        import json

        profile = session.exec(
            select(UserProfile).where(UserProfile.user_id == user_id)
        ).first()

        if profile:
            # Deserialize notification preferences from JSON string to dict
            if isinstance(profile.notification_preferences, str):
                try:
                    profile.notification_preferences = json.loads(profile.notification_preferences)
                except (ValueError, TypeError):
                    # If parsing fails, use a default value
                    profile.notification_preferences = {"toast_notifications": True}

        return profile

    @staticmethod
    def update_profile(*, session: Session, user_id: UUID,
                      profile_update: 'UserProfileUpdate') -> Optional['UserProfile']:
        from ..models.profile import UserProfile

        profile = session.exec(
            select(UserProfile).where(UserProfile.user_id == user_id)
        ).first()

        if not profile:
            return None

        import json

        # Update fields if provided
        if profile_update.display_name is not None:
            profile.display_name = profile_update.display_name
        if profile_update.preferred_language is not None:
            profile.preferred_language = profile_update.preferred_language
        if profile_update.theme_preference is not None:
            profile.theme_preference = profile_update.theme_preference
        if profile_update.notification_preferences is not None:
            # Convert dict to JSON string for storage
            profile.notification_preferences = json.dumps(profile_update.notification_preferences)
        if profile_update.avatar is not None:
            profile.avatar = profile_update.avatar

        session.add(profile)
        session.commit()
        session.refresh(profile)

        return profile


class TaskShareService:
    """
    Service class for handling task sharing-related operations.
    """

    @staticmethod
    def create_task_share(*, session: Session, task_id: UUID, user_id: UUID,
                         role: 'RoleEnum') -> 'TaskShare':
        from ..models.task_share import TaskShare, RoleEnum

        # Create computed permissions based on role
        permissions = TaskShareService._compute_permissions(role)

        task_share = TaskShare(
            task_id=task_id,
            user_id=user_id,
            role=role,
            permissions=permissions
        )

        session.add(task_share)
        session.commit()
        session.refresh(task_share)

        return task_share

    @staticmethod
    def _compute_permissions(role: 'RoleEnum') -> dict:
        from ..models.task_share import RoleEnum

        if role == RoleEnum.owner:
            return {"read": True, "write": True, "delete": True, "manage_access": True}
        elif role == RoleEnum.editor:
            return {"read": True, "write": True, "delete": False, "manage_access": False}
        elif role == RoleEnum.viewer:
            return {"read": True, "write": False, "delete": False, "manage_access": False}
        else:
            # Default to viewer permissions for safety
            return {"read": True, "write": False, "delete": False, "manage_access": False}

    @staticmethod
    def get_task_shares_for_task(*, session: Session, task_id: UUID) -> List['TaskShare']:
        from ..models.task_share import TaskShare

        task_shares = session.exec(
            select(TaskShare).where(TaskShare.task_id == task_id)
        ).all()
        return task_shares

    @staticmethod
    def get_task_shares_for_user(*, session: Session, user_id: UUID) -> List['TaskShare']:
        from ..models.task_share import TaskShare

        task_shares = session.exec(
            select(TaskShare).where(TaskShare.user_id == user_id)
        ).all()
        return task_shares

    @staticmethod
    def delete_task_share(*, session: Session, task_id: UUID, user_id: UUID) -> bool:
        from ..models.task_share import TaskShare

        task_share = session.exec(
            select(TaskShare).where(
                TaskShare.task_id == task_id,
                TaskShare.user_id == user_id
            )
        ).first()

        if not task_share:
            return False

        session.delete(task_share)
        session.commit()

        return True


class NotificationService:
    """
    Service class for handling notification-related operations.
    """

    @staticmethod
    def create_notification(*, session: Session, user_id: UUID,
                          notification_type: 'NotificationTypeEnum',
                          title: str, message: str, read: bool = False) -> 'Notification':
        from ..models.notification import Notification, NotificationTypeEnum

        notification = Notification(
            user_id=user_id,
            type=notification_type,
            title=title,
            message=message,
            read=read
        )

        session.add(notification)
        session.commit()
        session.refresh(notification)

        return notification

    @staticmethod
    def get_notifications_for_user(*, session: Session, user_id: UUID,
                                  unread_only: bool = False) -> List['Notification']:
        from ..models.notification import Notification

        query = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            query = query.where(Notification.read == False)

        notifications = session.exec(query).all()
        return notifications

    @staticmethod
    def mark_notification_as_read(*, session: Session, notification_id: UUID,
                                 user_id: UUID) -> Optional['Notification']:
        from ..models.notification import Notification

        notification = session.get(Notification, notification_id)

        if not notification or str(notification.user_id) != str(user_id):
            return None

        notification.read = True

        session.add(notification)
        session.commit()
        session.refresh(notification)

        return notification

    @staticmethod
    def delete_notification(*, session: Session, notification_id: UUID,
                           user_id: UUID) -> bool:
        from ..models.notification import Notification

        notification = session.get(Notification, notification_id)

        if not notification or str(notification.user_id) != str(user_id):
            return False

        session.delete(notification)
        session.commit()

        return True