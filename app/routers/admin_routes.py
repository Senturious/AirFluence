from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from .database import get_db  # Twoje połączenie do bazy
from .models import Key  # Model klucza w SQLAlchemy
from .dependencies import get_current_admin  # Weryfikacja, czy użytkownik to admin

router = APIRouter()


@router.post("/auth/add-pre-registration-data/")
def add_pre_registration_data(
        key: str,
        devices: list[str] = None,
        tasks: list[str] = None,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_admin)  # Musi być admin
):
    # Znajdź klucz w bazie danych
    key_entry = db.query(Key).filter(Key.key == key).first()
    if not key_entry:
        raise HTTPException(status_code=404, detail="Key not found")

    if key_entry.is_used:
        raise HTTPException(status_code=400, detail="Key already used")

    # Dodaj dane urządzeń
    if devices:
        key_entry.devices = ",".join(devices) if not key_entry.devices else key_entry.devices + "," + ",".join(devices)

    # Dodaj zadania
    if tasks:
        key_entry.tasks = ",".join(tasks) if not key_entry.tasks else key_entry.tasks + "," + ",".join(tasks)

    db.commit()
    db.refresh(key_entry)

    return {"message": "Pre-registration data added successfully"}
