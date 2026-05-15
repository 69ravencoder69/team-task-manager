from fastapi import APIRouter, HTTPException

from app.config import get_settings
from app.seed import seed

router = APIRouter(prefix="/dev", tags=["Development"])
settings = get_settings()


@router.post("/seed")
@router.get("/seed")
def run_seed():
    """Run demo seed. Allowed when ENV=development or AUTO_SEED is enabled."""
    if settings.env != "development" and not settings.auto_seed:
        raise HTTPException(status_code=403, detail="Seed disabled in production. Set AUTO_SEED=true temporarily.")
    seed()
    return {"message": "Seed completed. Demo users: admin@demo.com / Admin123!"}
