from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.project_model import ProjectMemberRole, ProjectStatus


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: Optional[str] = None
    status: ProjectStatus = ProjectStatus.active


class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    status: Optional[ProjectStatus] = None


class ProjectMemberCreate(BaseModel):
    user_id: int
    role: ProjectMemberRole = ProjectMemberRole.member


class ProjectMemberResponse(BaseModel):
    id: int
    project_id: int
    user_id: int
    role: ProjectMemberRole
    user_email: Optional[str] = None
    user_name: Optional[str] = None

    model_config = {"from_attributes": True}


class ProjectResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    status: ProjectStatus
    created_by: int
    created_at: datetime
    member_count: Optional[int] = None
    task_count: Optional[int] = None

    model_config = {"from_attributes": True}
