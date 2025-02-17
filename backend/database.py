from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Creating database engine
engine = create_engine(DATABASE_URL)

# Creating sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Baseclass for SQLAlchemy models
Base = declarative_base()

# Dependency for session control in FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

