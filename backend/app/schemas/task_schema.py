from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.task_model import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    project_id: int
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.todo
    priority: TaskPriority = TaskPriority.medium
    due_date: Optional[date] = None
    assigned_to: Optional[int] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[date] = None
    assigned_to: Optional[int] = None


class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class CommentCreate(BaseModel):
    content: str = Field(min_length=1)


class CommentResponse(BaseModel):
    id: int
    task_id: int
    user_id: int
    content: str
    created_at: datetime
    user_name: Optional[str] = None

    model_config = {"from_attributes": True}


class TaskResponse(BaseModel):
    id: int
    project_id: int
    title: str
    description: Optional[str]
    status: TaskStatus
    priority: TaskPriority
    due_date: Optional[date]
    assigned_to: Optional[int]
    created_by: int
    created_at: datetime
    project_name: Optional[str] = None
    assignee_name: Optional[str] = None

    model_config = {"from_attributes": True}
