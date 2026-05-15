from datetime import date
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.middleware.auth_middleware import is_project_member
from app.models.comment_model import Comment
from app.models.project_model import Project, ProjectMember
from app.models.task_model import Task, TaskStatus
from app.models.user_model import User, UserRole
from app.schemas.task_schema import CommentCreate, TaskCreate, TaskResponse, TaskUpdate
from app.utils.validators import is_overdue


def _to_response(task: Task, db: Session) -> TaskResponse:
    project = db.query(Project).filter(Project.id == task.project_id).first()
    assignee = db.query(User).filter(User.id == task.assigned_to).first() if task.assigned_to else None
    return TaskResponse(
        id=task.id,
        project_id=task.project_id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        assigned_to=task.assigned_to,
        created_by=task.created_by,
        created_at=task.created_at,
        project_name=project.name if project else None,
        assignee_name=assignee.full_name if assignee else None,
    )


def _accessible_project_ids(db: Session, user: User) -> list[int] | None:
    if user.role == UserRole.admin:
        return None
    return [m.project_id for m in db.query(ProjectMember).filter(ProjectMember.user_id == user.id).all()]


def list_tasks(
    db: Session,
    user: User,
    project_id: Optional[int] = None,
    status_filter: Optional[TaskStatus] = None,
    assigned_to: Optional[int] = None,
    search: Optional[str] = None,
) -> list[TaskResponse]:
    query = db.query(Task)

    project_ids = _accessible_project_ids(db, user)
    if project_ids is not None:
        if not project_ids:
            return []
        query = query.filter(Task.project_id.in_(project_ids))

    if project_id:
        if project_ids is not None and project_id not in project_ids:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this project")
        query = query.filter(Task.project_id == project_id)

    if status_filter:
        query = query.filter(Task.status == status_filter)

    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)

    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    tasks = query.order_by(Task.created_at.desc()).all()
    return [_to_response(t, db) for t in tasks]


def get_task(db: Session, task_id: int, user: User) -> TaskResponse:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if user.role != UserRole.admin and not is_project_member(db, user.id, task.project_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this project")

    return _to_response(task, db)


def create_task(db: Session, data: TaskCreate, user: User) -> TaskResponse:
    project = db.query(Project).filter(Project.id == data.project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    task = Task(
        project_id=data.project_id,
        title=data.title,
        description=data.description,
        status=data.status,
        priority=data.priority,
        due_date=data.due_date,
        assigned_to=data.assigned_to,
        created_by=user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return _to_response(task, db)


def update_task(db: Session, task_id: int, data: TaskUpdate, user: User) -> TaskResponse:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if user.role == UserRole.admin:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(task, key, value)
    else:
        if task.assigned_to != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Can only update your assigned tasks")
        if data.status is None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Members can only update task status")
        extra = data.model_dump(exclude_unset=True, exclude={"status"})
        if extra:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Members can only update task status")
        task.status = data.status

    db.commit()
    db.refresh(task)
    return _to_response(task, db)


def delete_task(db: Session, task_id: int) -> None:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    db.delete(task)
    db.commit()


def list_comments(db: Session, task_id: int, user: User) -> list[dict]:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if user.role != UserRole.admin and not is_project_member(db, user.id, task.project_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this project")

    comments = db.query(Comment).filter(Comment.task_id == task_id).order_by(Comment.created_at.desc()).all()
    result = []
    for c in comments:
        u = db.query(User).filter(User.id == c.user_id).first()
        result.append({
            "id": c.id,
            "task_id": c.task_id,
            "user_id": c.user_id,
            "content": c.content,
            "created_at": c.created_at,
            "user_name": u.full_name if u else None,
        })
    return result


def add_comment(db: Session, task_id: int, data: CommentCreate, user: User) -> dict:
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if user.role != UserRole.admin and not is_project_member(db, user.id, task.project_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this project")

    comment = Comment(task_id=task_id, user_id=user.id, content=data.content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return {
        "id": comment.id,
        "task_id": comment.task_id,
        "user_id": comment.user_id,
        "content": comment.content,
        "created_at": comment.created_at,
        "user_name": user.full_name,
    }
