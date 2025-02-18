from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.user import User
from app.services.auth_service import get_password_hash
from app.database import get_db

router = APIRouter()


@router.post("/users/")
def create_user(email: str, password: str, role: str, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(password)
    user = User(email=email, hashed_password=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
