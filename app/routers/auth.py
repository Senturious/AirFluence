import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.key import Key
from app.services.auth_service import get_password_hash, create_access_token, pwd_context
from app.dependencies import get_current_user, get_current_admin

router = APIRouter()

@router.post("/generate-key/")
def generate_registration_key(role: str, db: Session = Depends(get_db)):
    """
    Generate a one-time registration key for a given role.
    - Role can be: "Client", "Employee", "Manager", "Admin"
    """
    if role not in ["Client", "Employee", "Manager", "Admin"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid role. Valid roles are: Client, Employee, Manager, Admin."
        )

    generated_key = str(uuid.uuid4())  # Generate a unique key
    new_key = Key(key=generated_key, role=role)
    db.add(new_key)
    db.commit()
    return {"registration_key": generated_key, "role": role}

@router.post("/add-pre-registration-data/")
def add_pre_registration_data(
        key: str,
        devices: list[str] = None,
        tasks: list[str] = None,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_admin)  # Dependency that ensures only admin users can access
):
    """
    Add devices or tasks to a registration key before it is used.
    """
    # Find the key in the database
    key_entry = db.query(Key).filter(Key.key == key).first()
    if not key_entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Key not found!"
        )

    if key_entry.is_used:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Key has already been used.",
        )

    # Add devices to the key
    if devices:
        # Convert devices to a comma-separated string
        key_entry.devices = ",".join(devices) if not key_entry.devices else key_entry.devices + "," + ",".join(devices)

    # Add tasks to the key
    if tasks:
        key_entry.tasks = ",".join(tasks) if not key_entry.tasks else key_entry.tasks + "," + ",".join(tasks)

    db.commit()
    db.refresh(key_entry)

    return {"message": "Additional pre-registration data added successfully!", "key": key}

@router.post("/register/")
def register_user(email: str, password: str, unique_key: str, db: Session = Depends(get_db)):
    """
    Register a new user with a unique registration key.
    """
    # Validate the registration key
    key = db.query(Key).filter(Key.key == unique_key, Key.is_used == False).first()
    if not key:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or already used key.",
        )

    # Check if email already exists
    user_exists = db.query(User).filter(User.email == email).first()
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    # Hash the password
    hashed_password = get_password_hash(password)

    # Create a new User entry
    new_user = User(
        email=email,
        hashed_password=hashed_password,
        role=key.role,
        devices=key.devices,  # Assign devices from the registration key
        tasks=key.tasks  # Assign tasks from the registration key
    )
    db.add(new_user)

    # Mark the key as used
    key.is_used = True
    db.commit()

    return {"message": f"User registered successfully as {key.role}!"}

@router.post("/login/")
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Wyszukaj użytkownika na podstawie e-maila
    user = db.query(User).filter(User.email == form_data.username).first()

    if not pwd_context.verify(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


    # Tworzymy token JWT
    access_token = create_access_token(data={"sub": user.email, "role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}