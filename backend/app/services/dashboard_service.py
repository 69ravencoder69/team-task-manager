from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.middleware.auth_middleware import is_project_member
from app.models.project_model import Project, ProjectMember, ProjectStatus
from app.models.task_model import Task, TaskPriority, TaskStatus
from app.models.user_model import User, UserRole


def get_stats(db: Session, user: User) -> dict:
    if user.role == UserRole.admin:
        total_projects = db.query(Project).count()
        active_projects = db.query(Project).filter(Project.status == ProjectStatus.active).count()
        tasks_query = db.query(Task)
    else:
        project_ids = [m.project_id for m in db.query(ProjectMember).filter(ProjectMember.user_id == user.id).all()]
        total_projects = len(project_ids)
        active_projects = (
            db.query(Project)
            .filter(Project.id.in_(project_ids), Project.status == ProjectStatus.active)
            .count()
            if project_ids
            else 0
        )
        tasks_query = db.query(Task).filter(Task.project_id.in_(project_ids)) if project_ids else db.query(Task).filter(False)

    total_tasks = tasks_query.count()
    todo_tasks = tasks_query.filter(Task.status == TaskStatus.todo).count()
    in_progress_tasks = tasks_query.filter(Task.status == TaskStatus.in_progress).count()
    done_tasks = tasks_query.filter(Task.status == TaskStatus.done).count()

    all_tasks = tasks_query.all()
    overdue_count = sum(1 for t in all_tasks if t.due_date and t.due_date < date.today() and t.status != TaskStatus.done)

    my_open_tasks = (
        db.query(Task)
        .filter(Task.assigned_to == user.id, Task.status != TaskStatus.done)
        .count()
    )

    return {
        "total_projects": total_projects,
        "active_projects": active_projects,
        "total_tasks": total_tasks,
        "todo_tasks": todo_tasks,
        "in_progress_tasks": in_progress_tasks,
        "done_tasks": done_tasks,
        "overdue_count": overdue_count,
        "my_open_tasks": my_open_tasks,
    }


def get_analytics(db: Session, user: User) -> dict:
    if user.role == UserRole.admin:
        tasks = db.query(Task).all()
    else:
        project_ids = [m.project_id for m in db.query(ProjectMember).filter(ProjectMember.user_id == user.id).all()]
        tasks = db.query(Task).filter(Task.project_id.in_(project_ids)).all() if project_ids else []

    by_status = {s.value: 0 for s in TaskStatus}
    by_priority = {p.value: 0 for p in TaskPriority}
    by_assignee: dict[str, int] = {}

    for t in tasks:
        by_status[t.status.value] = by_status.get(t.status.value, 0) + 1
        by_priority[t.priority.value] = by_priority.get(t.priority.value, 0) + 1

        if user.role == UserRole.admin and t.assigned_to:
            assignee = db.query(User).filter(User.id == t.assigned_to).first()
            name = assignee.full_name if assignee else "Unassigned"
            by_assignee[name] = by_assignee.get(name, 0) + 1

    return {
        "tasks_by_status": by_status,
        "tasks_by_priority": by_priority,
        "tasks_by_assignee": by_assignee,
    }
