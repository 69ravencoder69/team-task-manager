# Local Testing (No Railway)

Uses **SQLite** — no MySQL or Railway needed.

## Quick start

**Terminal 1 — Backend:**
```powershell
cd team-task-manager\backend
pip install -r requirements.txt
python -m app.seed
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```powershell
cd team-task-manager\frontend
pip install -r requirements.txt
streamlit run app.py
```

## Links

| Service | URL |
|---------|-----|
| **App (open this)** | http://localhost:8501 |
| API docs | http://localhost:8000/docs |
| Health check | http://localhost:8000/health |

## Demo logins

| Email | Password | Role |
|-------|----------|------|
| admin@demo.com | Admin123! | admin |
| alex@demo.com | Member123! | member |
