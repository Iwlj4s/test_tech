from typing import Optional
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from starlette import status
from DAO.admin_dao import AdminDAO
from DAO.user_dao import UserDAO
from services.user_services import UserService
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

    # This all checks can be in excpetion_helper.py or in something like that
    if not user_to_promote.is_active:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User {user_to_promote.name} is not active"
            )

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

    user_data = await UserService.create_user_response(user=user_to_promote)

    return response_schemas.UserUpdateResponse(
        message=f"User {user_to_promote.name} has been {'promoted to admin' if is_admin else 'demoted from admin'}",
        status_code=200,
        data=user_data
    )

async def delete_user_admin(admin_user: models.User,
                            user_id: int,
                            deletion_reason: Optional[str],
                            db: AsyncSession) -> response_schemas.UserDeleteResponse:
    """
    Admin deletes another user's account.
    
    :param admin_user: Admin user
    :param user_id: ID of user to delete
    :param deletion_reason: Reason for deletion
    :param db: Database session
    :return: Deletion response
    """
    # Admin cannot delete themselves via this endpoint
    if admin_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admins cannot delete their own account via admin endpoint. Use self-delete instead."
        )
    
    # Get target user
    target_user = await UserDAO.get_user_by_id(db=db, user_id=user_id)
    
    await CheckHTTP404NotFound(founding_item=target_user,
                               text="User not found")
    
    # Check if already deleted
    if not target_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User account is already deleted"
        )
    
    deleted_user_name = target_user.name
    
    # Require deletion reason for admin deletions
    if not deletion_reason or len(deletion_reason.strip()) < 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Deletion reason is required (min 5 characters)"
        )
    
    # Soft delete user
    await UserDAO.soft_delete_acc(db=db,user_id=user_id,
                                  deleted_by_admin=True,
                                  deletion_reason=deletion_reason)
    
    # Delete user's posts (hard delete)
    deleted_posts_count = await UserDAO.soft_delete_user_posts(db=db,
                                                               user_id=user_id)
    
    return response_schemas.UserDeleteResponse(
        message=f"User {deleted_user_name} has been deleted by admin. {deleted_posts_count} posts removed.",
        status_code=200,
        deletion_reason=deletion_reason)


async def get_deleted_users_list(admin_user: models.User,
                                 db: AsyncSession) -> response_schemas.UserListResponse:
    """
    Get list of all deleted users (admin only).
    
    :param admin_user: Admin user
    :param db: Database session
    :return: List of deleted users
    """
    # Check admin permissions
    if not admin_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    deleted_users = await UserDAO.get_deleted_users(db=db)
    
    # Convert to response schema
    users_list = await UserService.get_formated_users(users=deleted_users)


    return users_list