# routes/admin_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import models, response_schemas, schema
from database.database import get_db
from repository import admin_repository
from helpers.admin_helper import require_admin

from helpers.exception_helper import CheckHTTP404NotFound

admin_router = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(require_admin)])  # All routes required admin rights

@admin_router.patch("/users/promote_to_admin/{user_id}")
async def promote_user_to_admin(user_id: int,
                                db: AsyncSession = Depends(get_db),
                                admin: models.User = Depends(require_admin)) -> response_schemas.UserUpdateResponse:
    """
    Promote a user to admin status.
    Only accessible by admins.
    """
    return await admin_repository.update_admin_status(user_id=user_id,
                                                      admin_user=admin,
                                                      is_admin=True,
                                                      db=db)

@admin_router.patch("/users/demote_from_admin/{user_id}")
async def demote_user_from_admin(user_id: int,
                               db: AsyncSession = Depends(get_db),
                               admin: models.User = Depends(require_admin)) -> response_schemas.UserUpdateResponse:
    """
    Demote a user from admin status.
    Only accessible by admins.
    """
    return await admin_repository.update_admin_status(user_id=user_id,
                                                      admin_user=admin,
                                                      is_admin=False,
                                                      db=db)

@admin_router.delete("/users/delete/{user_id}", status_code=200)
async def delete_user_admin(user_id: int,
                            deletion_data: schema.UserAdminDelete,
                            db: AsyncSession = Depends(get_db),
                            admin: models.User = Depends(require_admin)) -> response_schemas.UserDeleteResponse:
    """
    Admin deletes a user account.
    Only accessible by admins.
    
    - **user_id**: ID of user to delete
    - **deletion_data**: Deletion reason (required)
    
    Returns deletion confirmation with reason.
    """
    return await admin_repository.delete_user_admin(admin_user=admin,
                                                    user_id=user_id,
                                                    deletion_reason=deletion_data.reason,
                                                    db=db)

@admin_router.get("/users/deleted", status_code=200)
async def get_deleted_users(db: AsyncSession = Depends(get_db),
                            admin: models.User = Depends(require_admin)) -> response_schemas.UserListResponse:
    """
    Get list of all deleted users.
    Only accessible by admins.
    
    Returns list of deleted users with deletion info.
    """
    deleted_users = await admin_repository.get_deleted_users_list(admin_user=admin,
                                                                  db=db)
    
    await CheckHTTP404NotFound(founding_item=deleted_users, text="Deleted users not found")
    
    return response_schemas.UserListResponse(message="Deleted users retrieved successfully",
                                             status_code=200,
                                             data=deleted_users)