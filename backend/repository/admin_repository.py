from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from DAO.admin_dao import AdminDAO
from database import models, response_schemas
from helpers.exception_helper import CheckHTTP404NotFound, CheckHTTP409Conflict, CheckHTTP403FORBIDDEN_BOOL
from helpers.token_helper import get_token, verify_token

from DAO.general_dao import GeneralDAO


"""
Admin business logic layer.
Handles user authentication, registration, and user-related operations.
"""

async def update_admin_status(user_id: int,
                              is_admin: bool,
                              admin_user: models.User,
                              db: AsyncSession) -> response_schemas.UserUpdateResponse:
    """
    Update any user's admin status.        

    :param user_id: ID of the user to update
    :param is_admin: New admin status (True or False)
    :param admin_user: Authenticated admin user
    :param db: Database session

    :return: Updated user data
    :raises HTTPException: 404 if user not found or 403 if updating another user's profile
    """
        
    user_to_promote = await GeneralDAO.get_record_by_id(record_id=user_id,
                                                        model=models.User,
                                                        db=db)
    await CheckHTTP404NotFound(founding_item=user_to_promote, text="User not found")

    if is_admin:
        if user_to_promote.is_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {user_to_promote.name} is already an admin"
            )

        if user_to_promote.id == admin_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins cannot change their own admin status"
            )
    
    elif not is_admin:
        if not user_to_promote.is_admin:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {user_to_promote.name} is not an admin"
            )

        if user_to_promote.id == admin_user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admins cannot change their own admin status"
            )

    user_to_promote = await AdminDAO.update_user_admin_status(db=db, user=user_to_promote, is_admin=is_admin)

    return response_schemas.UserUpdateResponse(
        message=f"User {user_to_promote.name} has been {'promoted to admin' if is_admin else 'demoted from admin'}",
        status_code=200,
        data=response_schemas.UserResponse(
            id=user_to_promote.id,
            name=user_to_promote.name,
            email=user_to_promote.email,
            bio=user_to_promote.bio,
            location=user_to_promote.location,
            created_at=user_to_promote.created_at,
            is_admin=user_to_promote.is_admin
        )
    )