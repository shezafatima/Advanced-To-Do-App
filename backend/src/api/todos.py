from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional
from uuid import UUID
from ..database.session import get_session
from ..models.todo import (
    Todo, TodoCreate, TodoUpdate, TodoToggle, TodoRead, TodoAdvancedRead, PriorityEnum
)
from ..models.user import User
from ..models.tag import TagCreate
from ..services.todo_service import (
    TodoService, TagService, TaskShareService
)
from ..models.task_share import RoleEnum
from ..auth.utils import get_current_user
from ..utils.errors import TodoNotFoundException, UnauthorizedAccessException


router = APIRouter()


@router.get("/", response_model=List[TodoRead])
async def get_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all todos for the current user.
    """
    todos = TodoService.get_todos_for_user(session=session, user_id=current_user.id)
    return todos


from datetime import datetime, timezone

@router.get("/advanced", response_model=List[TodoAdvancedRead])
async def get_advanced_todos(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    priority: Optional[str] = Query(None, description="Filter by priority: low, medium, high"),
    tag: Optional[str] = Query(None, description="Filter by tag name"),
    due_date_from: Optional[str] = Query(None, description="Filter by due date from (YYYY-MM-DD)"),
    due_date_to: Optional[str] = Query(None, description="Filter by due date to (YYYY-MM-DD)"),
    sort_by: Optional[str] = Query(None, description="Sort by: priority, due_date, created_date"),
    sort_order: Optional[str] = Query("desc", description="Sort order: asc or desc"),
    status: Optional[str] = Query(None, description="Filter by status: pending, completed")
):
    """
    Get user's tasks with advanced features (priorities, tags, due dates, etc.)
    with optional filtering and sorting.
    """
    # Get all advanced todos for the user
    todos = TodoService.get_advanced_todos_for_user(session=session, user_id=current_user.id)

    # Apply filters if provided (basic implementation - could be enhanced with actual filtering)
    filtered_todos = []
    for todo in todos:
        # Filter by priority if specified
        if priority and str(todo.priority) != priority:
            continue
        # Filter by status if specified
        if status:
            if status == "pending" and todo.completed:
                continue
            elif status == "completed" and not todo.completed:
                continue
        filtered_todos.append(todo)

    # Apply sorting if specified
    reverse_order = sort_order.lower() == "desc"

    if sort_by:
        if sort_by == "priority":
            filtered_todos.sort(key=lambda x: x.priority.value, reverse=reverse_order)
        elif sort_by == "due_date":
            def due_date_key(x):
                if x.due_date:
                    return datetime.fromisoformat(x.due_date.replace('Z', '+00:00'))
                else:
                    # For tasks without due dates, put them at the end (or beginning depending on sort order)
                    if reverse_order:
                        return datetime.min.replace(tzinfo=timezone.utc)
                    else:
                        return datetime.max.replace(tzinfo=timezone.utc)
            filtered_todos.sort(key=due_date_key, reverse=reverse_order)
        elif sort_by == "created_date":
            filtered_todos.sort(key=lambda x: x.created_at, reverse=reverse_order)

    return filtered_todos


@router.post("/", response_model=TodoRead)
async def create_todo(
    todo_create: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new todo for the current user.
    """
    todo = TodoService.create_todo(
        session=session,
        todo_create=todo_create,
        user_id=current_user.id
    )
    return todo


@router.post("/advanced", response_model=TodoAdvancedRead)
async def create_advanced_todo(
    todo_create: TodoCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task with advanced features.
    """
    from datetime import datetime, timezone

    # Create the todo with advanced properties
    todo = Todo(
        title=todo_create.title,
        description=todo_create.description,
        completed=getattr(todo_create, 'completed', False),
        user_id=current_user.id,
        priority=getattr(todo_create, 'priority', PriorityEnum.medium),
        due_date=getattr(todo_create, 'due_date', None),
        recurrence_rule=getattr(todo_create, 'recurrence_rule', None)
    )

    session.add(todo)
    session.commit()
    session.refresh(todo)

    # Process tags if provided
    tag_list = []
    if hasattr(todo_create, 'tags') and todo_create.tags:
        for tag_name in todo_create.tags:
            # Create or get tag by name
            tag = TagService.get_tag_by_name(session=session, name=tag_name)
            if not tag:
                # Create new tag with auto-assigned color
                tag_data = TagCreate(name=tag_name, color="#default")
                tag = TagService.create_tag(session=session, tag_create=tag_data)
            tag_list.append(tag)

    # Return the advanced todo with tags
    todo_dict = todo.dict()
    todo_dict['tags'] = [tag.dict() for tag in tag_list]
    return TodoAdvancedRead(**todo_dict)


@router.get("/{todo_id}", response_model=TodoRead)
async def get_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific todo by ID.
    """
    todo = TodoService.get_todo_by_id(
        session=session,
        todo_id=todo_id,
        user_id=current_user.id
    )

    if not todo:
        raise TodoNotFoundException(str(todo_id))

    return todo


@router.put("/{todo_id}", response_model=TodoAdvancedRead)
async def update_todo(
    todo_id: UUID,
    todo_update: TodoUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific todo by ID.
    """
    todo = TodoService.update_todo(
        session=session,
        todo_id=todo_id,
        todo_update=todo_update,
        user_id=current_user.id
    )

    if not todo:
        raise TodoNotFoundException(str(todo_id))

    # For now, return basic todo data without tags (will implement tag joins later)
    todo_dict = todo.dict()
    # Add empty tags list for now - in a real implementation, you would fetch associated tags
    todo_dict['tags'] = []
    return TodoAdvancedRead(**todo_dict)


@router.delete("/{todo_id}")
async def delete_todo(
    todo_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific todo by ID.
    """
    success = TodoService.delete_todo(
        session=session,
        todo_id=todo_id,
        user_id=current_user.id
    )

    if not success:
        raise TodoNotFoundException(str(todo_id))

    return {"message": "Todo deleted successfully"}


@router.patch("/{todo_id}/toggle", response_model=TodoRead)
async def toggle_todo(
    todo_id: UUID,
    todo_toggle: TodoToggle,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a specific todo.
    """
    todo = TodoService.toggle_todo_completion(
        session=session,
        todo_id=todo_id,
        todo_toggle=todo_toggle,
        user_id=current_user.id
    )

    if not todo:
        raise TodoNotFoundException(str(todo_id))

    return todo


@router.post("/{task_id}/share")
async def share_task(
    task_id: UUID,
    request: dict,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Share a task with another user.
    Expected request format: {"user_email": "email@example.com", "role": "editor"}
    """
    from datetime import datetime, timezone
    from sqlmodel import select

    # Extract request data
    user_email = request.get("user_email")
    role_str = request.get("role", "viewer")

    if not user_email:
        raise HTTPException(status_code=400, detail="user_email is required")

    # Validate role
    try:
        role = RoleEnum(role_str.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid role. Must be one of: {', '.join(RoleEnum.__members__.keys())}")

    # Find user by email
    from ..models.user import User as UserModel
    target_user = session.exec(
        select(UserModel).where(UserModel.email == user_email)
    ).first()

    if not target_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Prevent users from sharing tasks with themselves
    if str(target_user.id) == str(current_user.id):
        raise HTTPException(status_code=400, detail="Cannot share task with yourself")

    # Verify that the current user owns the task
    task = TodoService.get_todo_by_id(
        session=session,
        todo_id=task_id,
        user_id=current_user.id
    )

    if not task:
        raise HTTPException(status_code=401, detail="Unauthorized: You don't own this task")

    # Check if task is already shared with this user
    existing_share = session.exec(
        select(TaskShare).where(
            TaskShare.task_id == task_id,
            TaskShare.user_id == target_user.id
        )
    ).first()

    if existing_share:
        # Update the existing share instead of creating a duplicate
        existing_share.role = role
        existing_share.permissions = TaskShareService._compute_permissions(role)
        session.add(existing_share)
        session.commit()
        session.refresh(existing_share)

        return {
            "task_id": str(task_id),
            "shared_with": user_email,
            "role": role_str,
            "shared_at": existing_share.shared_at
        }
    else:
        # Create the task share
        task_share = TaskShareService.create_task_share(
            session=session,
            task_id=task_id,
            user_id=target_user.id,
            role=role
        )

        return {
            "task_id": str(task_id),
            "shared_with": user_email,
            "role": role_str,
            "shared_at": datetime.now(timezone.utc)
        }


@router.delete("/{task_id}/share/{user_id}")
async def remove_task_share(
    task_id: UUID,
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Remove a task share for a specific user.
    """
    # Verify that the current user owns the task
    task = TodoService.get_todo_by_id(
        session=session,
        todo_id=task_id,
        user_id=current_user.id
    )

    if not task:
        raise HTTPException(status_code=401, detail="Unauthorized: You don't own this task")

    # Check if task is shared with the specified user
    from ..models.task_share import TaskShare
    task_share = session.exec(
        select(TaskShare).where(
            TaskShare.task_id == task_id,
            TaskShare.user_id == user_id
        )
    ).first()

    if not task_share:
        raise HTTPException(status_code=404, detail="Task share not found")

    # Remove the task share
    session.delete(task_share)
    session.commit()

    return {
        "message": "Task share removed successfully",
        "task_id": str(task_id),
        "user_id": str(user_id)
    }


@router.get("/{task_id}/shares")
async def get_task_shares(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all users that a task is shared with.
    """
    # Verify that the current user owns the task
    task = TodoService.get_todo_by_id(
        session=session,
        todo_id=task_id,
        user_id=current_user.id
    )

    if not task:
        raise HTTPException(status_code=401, detail="Unauthorized: You don't own this task")

    # Get all shares for this task
    from ..models.task_share import TaskShare
    task_shares = session.exec(
        select(TaskShare).where(TaskShare.task_id == task_id)
    ).all()

    return {
        "task_id": str(task_id),
        "shares": [
            {
                "user_id": str(share.user_id),
                "role": share.role.value,
                "permissions": share.permissions,
                "shared_at": share.shared_at
            }
            for share in task_shares
        ]
    }