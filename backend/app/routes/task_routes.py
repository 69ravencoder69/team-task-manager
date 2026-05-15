from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import get_current_user, require_admin
from app.models.task_model import TaskStatus
from app.models.user_model import User
from app.schemas.task_schema import CommentCreate, CommentResponse, TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.get("", response_model=list[TaskResponse])
def list_tasks(
    project_id: Optional[int] = Query(None),
    status: Optional[TaskStatus] = Query(None),
    assigned_to: Optional[int] = Query(None),
    search: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return task_service.list_tasks(db, current_user, project_id, status, assigned_to, search)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return task_service.get_task(db, task_id, current_user)


@router.post("", response_model=TaskResponse)
def create_task(
    data: TaskCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return task_service.create_task(db, data, current_user)


@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return task_service.update_task(db, task_id, data, current_user)


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    task_service.delete_task(db, task_id)
    return {"message": "Task deleted"}


@router.get("/{task_id}/comments", response_model=list[CommentResponse])
def list_comments(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return task_service.list_comments(db, task_id, current_user)


@router.post("/{task_id}/comments", response_model=CommentResponse)
def add_comment(
    task_id: int,
    data: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return task_service.add_comment(db, task_id, data, current_user)
