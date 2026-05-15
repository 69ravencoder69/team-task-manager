# Deploy Frontend on Render + Backend on Railway

## Architecture

```text
Render     →  Streamlit frontend  (https://xxx.onrender.com)
Railway    →  FastAPI backend     (https://xxx.up.railway.app)
Railway    →  MySQL database
```

---

## Part 1 — Railway (Backend + MySQL) — do this first

### MySQL
1. Railway project → **+ New** → **Database** → **MySQL**

### Backend
1. **+ New** → **GitHub Repo** → your repo
2. **Settings** → **Root Directory:** `backend`
3. **Start Command:**
   ```text
   uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
4. **Variables:**

| Variable | Value |
|----------|--------|
| `DATABASE_URL` | Reference → MySQL → `MYSQL_URL` |
| `JWT_SECRET` | long random string |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` |
| `CORS_ORIGINS` | `https://YOUR-APP.onrender.com` (add after Render deploy) |
| `ENV` | `production` |
| `AUTO_SEED` | `true` (remove after first login works) |

5. **Networking** → **Generate Domain** → copy URL  
   Example: `https://team-task-manager-production.up.railway.app`

6. Test: open `https://YOUR-BACKEND.up.railway.app/health` → `{"status":"ok"}`

---

## Part 2 — Render (Frontend)

### Option A — Manual (recommended)

1. Go to [render.com](https://render.com) → sign in with GitHub
2. **New +** → **Web Service**
3. Connect your `team-task-manager` repository
4. Settings:

| Field | Value |
|-------|--------|
| **Name** | `team-task-manager-frontend` |
| **Region** | closest to you |
| **Branch** | `main` |
| **Root Directory** | `frontend` |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false` |
| **Plan** | Free |

5. **Environment Variables:**

| Key | Value |
|-----|--------|
| `API_BASE_URL` | Your Railway backend URL (no trailing slash) |
| `PYTHON_VERSION` | `3.11.9` |

Example:
```text
API_BASE_URL=https://team-task-manager-production.up.railway.app
```

6. Click **Create Web Service**
7. Wait for deploy (5–10 min on free tier)
8. Copy your Render URL: `https://team-task-manager-frontend.onrender.com`

### Option B — Blueprint

1. **New +** → **Blueprint**
2. Select repo (uses root `render.yaml`)
3. Set `API_BASE_URL` when prompted
4. Deploy

---

## Part 3 — Connect frontend ↔ backend

### Update Railway CORS

1. Railway → **backend** service → **Variables**
2. Set:
   ```text
   CORS_ORIGINS=https://team-task-manager-frontend.onrender.com
   ```
   (use your exact Render URL)
3. Redeploy backend

---

## Part 4 — Test

1. Open Render URL in browser
2. Login: `admin@demo.com` / `Admin123!`
3. If login fails → set `AUTO_SEED=true` on Railway, redeploy backend

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Build failed on Render | Root Directory must be `frontend` |
| Cannot connect to API | Check `API_BASE_URL` in Render env vars |
| CORS error | Update `CORS_ORIGINS` on Railway to Render URL |
| Render app sleeps (free) | First load takes 30–60 sec — normal on free plan |
| 502 on Render | Check Start Command uses `$PORT` |

---

## Do NOT use `frontend/.env` on Render

Set `API_BASE_URL` in **Render Dashboard → Environment**, not only in local `.env`.
