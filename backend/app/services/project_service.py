from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.middleware.auth_middleware import is_project_member
from app.models.project_model import Project, ProjectMember, ProjectMemberRole, ProjectStatus
from app.models.task_model import Task
from app.models.user_model import User, UserRole
from app.schemas.project_schema import ProjectCreate, ProjectMemberCreate, ProjectResponse, ProjectUpdate


def _to_response(project: Project, db: Session) -> ProjectResponse:
    member_count = db.query(ProjectMember).filter(ProjectMember.project_id == project.id).count()
    task_count = db.query(Task).filter(Task.project_id == project.id).count()
    return ProjectResponse(
        id=project.id,
        name=project.name,
        description=project.description,
        status=project.status,
        created_by=project.created_by,
        created_at=project.created_at,
        member_count=member_count,
        task_count=task_count,
    )


def list_projects(db: Session, user: User) -> list[ProjectResponse]:
    if user.role == UserRole.admin:
        projects = db.query(Project).order_by(Project.created_at.desc()).all()
    else:
        project_ids = [
            m.project_id
            for m in db.query(ProjectMember).filter(ProjectMember.user_id == user.id).all()
        ]
        projects = db.query(Project).filter(Project.id.in_(project_ids)).order_by(Project.created_at.desc()).all()
    return [_to_response(p, db) for p in projects]


def get_project(db: Session, project_id: int, user: User) -> ProjectResponse:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    if user.role != UserRole.admin and not is_project_member(db, user.id, project_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this project")
    return _to_response(project, db)


def create_project(db: Session, data: ProjectCreate, user: User) -> ProjectResponse:
    project = Project(
        name=data.name,
        description=data.description,
        status=data.status,
        created_by=user.id,
    )
    db.add(project)
    db.flush()

    db.add(
        ProjectMember(
            project_id=project.id,
            user_id=user.id,
            role=ProjectMemberRole.admin,
        )
    )
    db.commit()
    db.refresh(project)
    return _to_response(project, db)


def update_project(db: Session, project_id: int, data: ProjectUpdate) -> ProjectResponse:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)
    return _to_response(project, db)


def delete_project(db: Session, project_id: int) -> None:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db.delete(project)
    db.commit()


def add_member(db: Session, project_id: int, data: ProjectMemberCreate) -> dict:
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")

    target_user = db.query(User).filter(User.id == data.user_id).first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    existing = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id, ProjectMember.user_id == data.user_id)
        .first()
    )
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already a member")

    member = ProjectMember(project_id=project_id, user_id=data.user_id, role=data.role)
    db.add(member)
    db.commit()
    db.refresh(member)
    return {
        "id": member.id,
        "project_id": member.project_id,
        "user_id": member.user_id,
        "role": member.role,
        "user_email": target_user.email,
        "user_name": target_user.full_name,
    }


def remove_member(db: Session, project_id: int, user_id: int) -> None:
    member = (
        db.query(ProjectMember)
        .filter(ProjectMember.project_id == project_id, ProjectMember.user_id == user_id)
        .first()
    )
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    db.delete(member)
    db.commit()


def list_members(db: Session, project_id: int, user: User) -> list[dict]:
    if user.role != UserRole.admin and not is_project_member(db, user.id, project_id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not a member of this project")

    members = db.query(ProjectMember).filter(ProjectMember.project_id == project_id).all()
    result = []
    for m in members:
        u = db.query(User).filter(User.id == m.user_id).first()
        result.append({
            "id": m.id,
            "project_id": m.project_id,
            "user_id": m.user_id,
            "role": m.role,
            "user_email": u.email if u else None,
            "user_name": u.full_name if u else None,
        })
    return result
