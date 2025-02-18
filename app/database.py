from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:enterprise@localhost:5432/airfluence_db"  # Zmień na swoje dane

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

from app.models.user import User
from app.models.key import Key

# Funkcja pozwalająca uzyskać sesję DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

