# Team Task Manager

Production-ready team task management app: **Streamlit** frontend, **FastAPI** backend, **MySQL** on Railway, **JWT** authentication, Admin/Member RBAC.

## Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| Database | MySQL (Railway) |
| ORM | SQLAlchemy |
| Auth | JWT |

## Project Structure

```
team-task-manager/
├── backend/app/     # FastAPI API
├── frontend/        # Streamlit UI
├── railway.json
└── .env.example
```

## Demo Accounts (after seeding)

| Email | Password | Role |
|-------|----------|------|
| admin@demo.com | Admin123! | admin |
| alex@demo.com | Member123! | member |
| sam@demo.com | Member123! | member |
| jordan@demo.com | Member123! | member |

## Local Development

### 1. Environment

Copy `.env.example` to `backend/.env` and `frontend/.env`. Set `DATABASE_URL` to your Railway MySQL URL (use `mysql+pymysql://` prefix).

### 2. Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API docs: http://localhost:8000/docs

### 3. Seed database

```bash
cd backend
python -m app.seed
```

### 4. Frontend

```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

## Railway Deployment

### Step 1 — Create Railway Project

1. Go to [railway.app](https://railway.app) and create a new project.
2. Click **+ New** → **Database** → **MySQL**.
3. Open the MySQL service → **Variables** → copy `MYSQL_URL` or `DATABASE_URL`.

### Step 2 — Deploy Backend

1. **+ New** → **GitHub Repo** → connect your repo.
2. Set **Root Directory** to `backend`.
3. Add variables:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Your Railway MySQL URL (auto-linked if using reference) |
| `JWT_SECRET` | Long random string |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` |
| `CORS_ORIGINS` | Your frontend Railway URL (add after frontend deploy) |
| `ENV` | `production` |

4. Deploy. Note the public backend URL (e.g. `https://xxx.up.railway.app`).

### Step 3 — Deploy Frontend

1. **+ New** → same repo, **Root Directory** = `frontend`.
2. Add variable: `API_BASE_URL` = backend public URL.
3. Deploy. Note the frontend public URL.
4. Update backend `CORS_ORIGINS` to include the frontend URL and redeploy.

### Step 4 — Seed Database

In Railway backend service → **Shell**:

```bash
python -m app.seed
```

### Step 5 — Verify

- Backend health: `https://<backend>/health`
- API docs: `https://<backend>/docs`
- Frontend: open Streamlit URL, login with demo accounts above.

## API Overview

- `POST /auth/register`, `POST /auth/login`, `GET /auth/me`
- `GET/POST/PUT/DELETE /projects`
- `POST/DELETE /projects/{id}/members`
- `GET/POST/PUT/DELETE /tasks`
- `GET/POST /tasks/{id}/comments`
- `GET /dashboard/stats`, `GET /dashboard/analytics`
