from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


# Przykład operacji na zleceniach
@router.get("/")
def get_all_orders(db: Session = Depends(get_db)):
    return [{"id": 1, "status": "pending"}, {"id": 2, "status": "completed"}]
