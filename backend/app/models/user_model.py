import enum
from datetime import datetime

from sqlalchemy import DateTime, Enum, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    member = "member"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), default=UserRole.member, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    projects_created = relationship("Project", back_populates="creator", foreign_keys="Project.created_by")
    tasks_assigned = relationship("Task", back_populates="assignee", foreign_keys="Task.assigned_to")
    tasks_created = relationship("Task", back_populates="creator", foreign_keys="Task.created_by")
    comments = relationship("Comment", back_populates="user")
    project_memberships = relationship("ProjectMember", back_populates="user")
    notifications = relationship("Notification", back_populates="user")
