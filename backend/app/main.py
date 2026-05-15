from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.database import Base, engine
from app.models import Comment, Notification, Project, ProjectMember, Task, User  # noqa: F401
from app.routes import auth_routes, dashboard_routes, dev_routes, project_routes, task_routes, user_routes

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    if settings.auto_seed or settings.env == "development":
        try:
            from app.seed import seed
            seed()
        except Exception:
            pass
    yield


app = FastAPI(
    title="Team Task Manager API",
    description="FastAPI backend for team task management",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router)
app.include_router(project_routes.router)
app.include_router(task_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(user_routes.router)
app.include_router(dev_routes.router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def root():
    return {"message": "Team Task Manager API", "docs": "/docs"}
