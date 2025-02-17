from fastapi import APIRouter, Depends, HTTPException, Security
from sqlalchemy.orm import Session
from database import get_db
from app import models, schemas, auth
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.auth import SECRET_KEY, ALGORITHM
from app.schemas import UserResponse

router = APIRouter()

# User registration
@router.post("/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = auth.hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed_password)

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return schemas.UserResponse(
        id=db_user.id,
        name=db_user.name,
        email=db_user.email
    )

# OAuth2 authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")

# Retrieve current authenticated user
def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise credentials_exception
    return user

# Get details of the authenticated user
@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")

    return schemas.UserResponse(
        id=current_user.id,
        name=current_user.name,
        email=current_user.email
    )