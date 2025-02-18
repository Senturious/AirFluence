from fastapi import Depends, HTTPException, status
from app.models.user import User  # Zakładamy, że taki model istnieje


async def get_current_user() -> User:
    """Logika pobierania użytkownika"""
    # Tutaj zwracamy przykład użytkownika; zastąp prawdziwą logiką
    return User(email="example@example.com", role="user")


async def get_current_admin(user: User = Depends(get_current_user)) -> User:
    """Logika weryfikująca użytkownika jako administratora"""
    if user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have admin privileges"
        )
    return user
