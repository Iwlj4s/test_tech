from sqlalchemy import select, update, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional

from DAO.general_dao import GeneralDAO
from database import response_schemas
from database import models
from helpers import exception_helper
from services.user_services import UserService


class AdminDAO:
    """
    Data Access Object for Admin.
    Contains user-specific database operations.
    """
    @classmethod
    async def update_user_admin_status(cls,
                                       db: AsyncSession,
                                       user: models.User,
                                       is_admin: bool) -> models.User:
        """
        Update user's admin status.
        
        :param db: Database session
        :param user: User object to update
        :param is_admin: New admin status
        :return: Updated User object
        """

        user.is_admin = is_admin
        await db.commit()
        await db.refresh(user)
        
        return user