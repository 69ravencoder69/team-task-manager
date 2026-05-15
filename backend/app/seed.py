"""Idempotent seed script. Run: python -m app.seed (from backend/)"""
from datetime import date, timedelta

from app.database import SessionLocal, engine, Base
from app.models import Comment, Notification, Project, ProjectMember, Task, User
from app.models.project_model import ProjectMemberRole, ProjectStatus
from app.models.task_model import TaskPriority, TaskStatus
from app.models.user_model import UserRole
from app.utils.password_handler import hash_password

DEMO_USERS = [
    {"email": "admin@demo.com", "password": "Admin123!", "full_name": "Admin User", "role": UserRole.admin},
    {"email": "alex@demo.com", "password": "Member123!", "full_name": "Alex Rivera", "role": UserRole.member},
    {"email": "sam@demo.com", "password": "Member123!", "full_name": "Sam Chen", "role": UserRole.member},
    {"email": "jordan@demo.com", "password": "Member123!", "full_name": "Jordan Lee", "role": UserRole.member},
]


def get_or_create_user(db, data: dict) -> User:
    user = db.query(User).filter(User.email == data["email"]).first()
    if user:
        return user
    user = User(
        email=data["email"],
        hashed_password=hash_password(data["password"]),
        full_name=data["full_name"],
        role=data["role"],
    )
    db.add(user)
    db.flush()
    return user


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        if db.query(User).filter(User.email == "admin@demo.com").first():
            print("Seed data already exists. Skipping.")
            return

        users = {u["email"]: get_or_create_user(db, u) for u in DEMO_USERS}
        admin = users["admin@demo.com"]
        alex = users["alex@demo.com"]
        sam = users["sam@demo.com"]
        jordan = users["jordan@demo.com"]

        project1 = Project(
            name="FSAE Vehicle Design",
            description="Formula SAE vehicle design and engineering tasks",
            status=ProjectStatus.active,
            created_by=admin.id,
        )
        project2 = Project(
            name="Sponsor Outreach Q2",
            description="Q2 sponsor outreach and partnership development",
            status=ProjectStatus.active,
            created_by=admin.id,
        )
        db.add_all([project1, project2])
        db.flush()

        members_p1 = [
            ProjectMember(project_id=project1.id, user_id=admin.id, role=ProjectMemberRole.admin),
            ProjectMember(project_id=project1.id, user_id=alex.id, role=ProjectMemberRole.member),
            ProjectMember(project_id=project1.id, user_id=sam.id, role=ProjectMemberRole.member),
            ProjectMember(project_id=project1.id, user_id=jordan.id, role=ProjectMemberRole.member),
        ]
        members_p2 = [
            ProjectMember(project_id=project2.id, user_id=admin.id, role=ProjectMemberRole.admin),
            ProjectMember(project_id=project2.id, user_id=alex.id, role=ProjectMemberRole.member),
            ProjectMember(project_id=project2.id, user_id=jordan.id, role=ProjectMemberRole.member),
        ]
        db.add_all(members_p1 + members_p2)

        tasks_data = [
            (project1.id, "CAD wing mount", alex.id, TaskStatus.in_progress, TaskPriority.high),
            (project1.id, "Brake bias spreadsheet", sam.id, TaskStatus.todo, TaskPriority.medium),
            (project1.id, "Cost report draft", jordan.id, TaskStatus.done, TaskPriority.low),
            (project2.id, "Sponsor email template", alex.id, TaskStatus.todo, TaskPriority.high),
            (project2.id, "Meeting slides", jordan.id, TaskStatus.in_progress, TaskPriority.medium),
        ]

        tasks = []
        for i, (pid, title, assignee_id, status, priority) in enumerate(tasks_data):
            task = Task(
                project_id=pid,
                title=title,
                description=f"Demo task: {title}",
                status=status,
                priority=priority,
                due_date=date.today() + timedelta(days=7 - i),
                assigned_to=assignee_id,
                created_by=admin.id,
            )
            tasks.append(task)
        db.add_all(tasks)
        db.flush()

        comments = [
            Comment(task_id=tasks[0].id, user_id=alex.id, content="Started initial CAD model for the wing mount."),
            Comment(task_id=tasks[0].id, user_id=admin.id, content="Please review stress analysis before finalizing."),
            Comment(task_id=tasks[3].id, user_id=jordan.id, content="Draft slides ready for review by Friday."),
        ]
        db.add_all(comments)

        notifications = [
            Notification(user_id=alex.id, message="You were assigned: CAD wing mount", is_read=False),
            Notification(user_id=sam.id, message="New task: Brake bias spreadsheet", is_read=False),
            Notification(user_id=jordan.id, message="Task due soon: Meeting slides", is_read=True),
        ]
        db.add_all(notifications)

        db.commit()
        print("Seed completed successfully!")
        print("Demo accounts:")
        for u in DEMO_USERS:
            print(f"  {u['email']} / {u['password']} ({u['role'].value})")

    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
