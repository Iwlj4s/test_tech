# routes/admin_router.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import models, response_schemas, schema
from database.database import get_db
from repository import admin_repository
from helpers.admin_helper import require_admin

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