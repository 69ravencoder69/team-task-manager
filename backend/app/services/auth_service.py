from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user_model import User, UserRole
from app.schemas.user_schema import UserCreate, UserLogin
from app.utils.jwt_handler import create_access_token
from app.utils.password_handler import hash_password, verify_password


def register_user(db: Session, data: UserCreate) -> User:
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    user_count = db.query(User).count()
    role = UserRole.admin if user_count == 0 else UserRole.member

    user = User(
        email=data.email,
        hashed_password=hash_password(data.password),
        full_name=data.full_name,
        role=role,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(db: Session, data: UserLogin) -> tuple[User, str]:
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")

    token = create_access_token(user.id, user.role.value)
    return user, token
