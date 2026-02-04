from fastapi import Depends, HTTPException, status
from repository.user_repository import get_current_user
from database import models

async def check_is_admin(current_user: models.User) -> None:
    """
    Check if current user is admin.
    Raises HTTPException if not admin.
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )

async def require_admin(current_user: models.User = Depends(get_current_user)) -> models.User:
    """
    Dependency that requires admin role.
    """
    check_is_admin(current_user)
    return current_user