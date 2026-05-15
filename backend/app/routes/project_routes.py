from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import get_current_user, require_admin
from app.models.user_model import User
from app.schemas.project_schema import ProjectCreate, ProjectMemberCreate, ProjectResponse, ProjectUpdate
from app.services import project_service

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.get("", response_model=list[ProjectResponse])
def list_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return project_service.list_projects(db, current_user)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return project_service.get_project(db, project_id, current_user)


@router.post("", response_model=ProjectResponse)
def create_project(
    data: ProjectCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return project_service.create_project(db, data, current_user)


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return project_service.update_project(db, project_id, data)


@router.delete("/{project_id}")
def delete_project(
    project_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    project_service.delete_project(db, project_id)
    return {"message": "Project deleted"}


@router.get("/{project_id}/members")
def list_members(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return project_service.list_members(db, project_id, current_user)


@router.post("/{project_id}/members")
def add_member(
    project_id: int,
    data: ProjectMemberCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return project_service.add_member(db, project_id, data)


@router.delete("/{project_id}/members/{user_id}")
def remove_member(
    project_id: int,
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    project_service.remove_member(db, project_id, user_id)
    return {"message": "Member removed"}
