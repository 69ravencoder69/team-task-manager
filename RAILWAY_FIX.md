# Railway Build Failed — Fix Guide

## Why `backend/.env` does NOT work on Railway

`backend/.env` is in `.gitignore` → it is **never uploaded** to GitHub/Railway.

Put variables in: **Railway → Backend service → Variables tab** (not in a file).

---

## Fix the "Build image" failure

### Step 1 — Correct Root Directory (MOST IMPORTANT)

1. Open your **backend** service on Railway (not MySQL).
2. **Settings** → **Root Directory**
3. Set exactly: `backend`
4. Save

If Root Directory is empty or wrong, Railway builds the wrong folder and fails.

### Step 2 — Start Command

**Settings** → **Deploy** → **Start Command**:

```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Step 3 — Variables (Railway dashboard, NOT .env file)

Click **Variables** → **Add Variable**:

| Name | Value |
|------|--------|
| `DATABASE_URL` | Click **Add Reference** → select MySQL → `MYSQL_URL` |
| `JWT_SECRET` | any long random string |
| `JWT_ALGORITHM` | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `1440` |
| `CORS_ORIGINS` | your frontend URL (or `*` temporarily) |
| `ENV` | `production` |
| `AUTO_SEED` | `true` (first deploy only, remove later) |

### Step 4 — Push latest code to GitHub

```powershell
cd "c:\Users\LAKSHAY CHHABRA\Desktop\FSAE\team-task-manager"
git add .
git commit -m "Fix Railway backend build"
git push
```

Railway will redeploy automatically.

### Step 5 — Check build logs

**Deployments** → failed deploy → **View logs**

Look for red error text at the bottom.

---

## Common mistakes

| Mistake | Fix |
|---------|-----|
| Root Directory empty | Set to `backend` |
| Only created `backend/.env` | Use Railway **Variables** tab |
| Service named "requirements" | Rename or create new service from repo with root `backend` |
| Wrong variable name | Use `DATABASE_URL` (reference MySQL `MYSQL_URL`) |
| Pasted backend URL as DATABASE_URL | Use **MySQL** connection URL, not `https://...` |

---

## After successful deploy

1. Open `https://YOUR-BACKEND.up.railway.app/health` → should show `{"status":"ok"}`
2. Open `https://YOUR-BACKEND.up.railway.app/docs`
3. Login on frontend with `admin@demo.com` / `Admin123!`
