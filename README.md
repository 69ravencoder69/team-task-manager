# Team Task Manager

Production-ready team task management app: **Streamlit** frontend, **FastAPI** backend, **MySQL** on Railway, **JWT** authentication, Admin/Member RBAC.

## Stack & Hosting

| Layer | Technology | Hosting |
|-------|------------|---------|
| Frontend | Streamlit | Render / Railway |
| Backend | FastAPI | Railway |
| Database | MySQL | Railway |
| ORM | SQLAlchemy | - |
| Auth | JWT | - |

## Project Structure

```
team-task-manager/
├── backend/app/     # FastAPI API
├── frontend/        # Streamlit UI
├── railway.json
└── .env.example
```

## Key Features & Customizations

- **Vibrant & Bright Interactive Analytics**: Features high-contrast, colorful custom Plotly charts (status donut charts, priority bar charts, and horizontal assignee bar charts) designed to pop against dark mode and replace plain grayscale elements.
- **Top Header Bar with Quick Actions**: Premium top bar rendering a consistent logo header, Light/Dark theme buttons, and a handy **🔄 Refresh** button on internal pages for instantaneous cache clearance.
- **Unified User Sidebar**: Quick navigation controls (Dashboard, Projects, Tasks, Analytics) that auto-adapt based on authorization level.
- **Granular RBAC (Role-Based Access Control)**:
  - **Admins**: Access to full creation, modification, and deletion endpoints for projects and tasks, plus assignee/member controls.
  - **Members**: Responsive views for assigned tasks, individual status management, and real-time comments.
- **Cross-page Session Redirection**: Intuitively remembers where you wanted to go (e.g. Analytics, Projects) and redirects you there post-login.

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

## Deployment (Railway & Render)

### Step 1 — Create Railway Project

1. Go to [railway.app](https://railway.app) and create a new project.
2. Click **+ New** → **Database** → **MySQL**.
3. Open the MySQL service → **Variables** → copy `MYSQL_URL` or `DATABASE_URL`.

### Step 2 — Deploy Backend (Railway)

1. **+ New** → **GitHub Repo** → connect your repo.
2. Set **Root Directory** to `backend`.
3. Add variables:

| Variable | Value |
|----------|-------|
| `DATABASE_URL` | Your Railway MySQL URL (auto-linked if using reference) |
| `JWT_SECRET` | Long random string |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` |
| `CORS_ORIGINS` | Your frontend Render/Railway URL (add after frontend deploy) |
| `ENV` | `production` |

4. Deploy. Note the public backend URL (e.g. `https://xxx.up.railway.app`).

### Step 3 — Deploy Frontend

#### Option A: Deploy Frontend on Render (Recommended)
1. Go to [render.com](https://render.com) and log in with GitHub.
2. Click **New +** → **Web Service** and link your repo.
3. Configure the following fields:
   - **Root Directory**: `frontend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false`
   - **Plan**: Free
4. Add the following **Environment Variables**:
   - `API_BASE_URL`: Your Railway backend URL (no trailing slash)
   - `PYTHON_VERSION`: `3.11.9`
5. Click **Create Web Service**.
> [!IMPORTANT]  
> Because Render uses free-tier instances for this service, **cold starts may take up to 1 minute to spin up or wake up the frontend** if it has been inactive. This is expected behavior.

#### Option B: Deploy Frontend on Railway
1. **+ New** → same repo, **Root Directory** = `frontend`.
2. Add variable: `API_BASE_URL` = backend public URL.
3. Deploy. Note the frontend public URL.

### Step 4 — Connect Frontend ↔ Backend (CORS)
Update the backend `CORS_ORIGINS` environment variable on Railway to include your frontend URL (either your `.onrender.com` domain or Railway domain) and redeploy the backend service.

### Step 5 — Seed Database

In Railway backend service → **Shell**:

```bash
python -m app.seed
```

### Step 6 — Verify

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
