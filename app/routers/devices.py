from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

router = APIRouter()


# Przykład zarządzania urządzeniami
@router.get("/")
def get_all_devices(db: Session = Depends(get_db)):
    return [{"id": 1, "name": "Device 1"}, {"id": 2, "name": "Device 2"}]
