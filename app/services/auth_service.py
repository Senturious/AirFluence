from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

# Password hashing configuration using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Secret key and algorithm for JWT
SECRET_KEY = "your-secret-key"  # Replace with a stronger key in production
ALGORITHM = "HS256"


# Function to hash a password
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


# Function to create a JWT access token
def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
