from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base


class Key(Base):
    __tablename__ = "keys"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False)
    is_used = Column(Boolean, default=False)
    devices = Column(String, nullable=True)
    tasks = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
