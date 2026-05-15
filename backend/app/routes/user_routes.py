from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.middleware.auth_middleware import require_admin
from app.models.user_model import User
from app.schemas.user_schema import UserBrief

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=list[UserBrief])
def list_users(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return db.query(User).order_by(User.full_name).all()
