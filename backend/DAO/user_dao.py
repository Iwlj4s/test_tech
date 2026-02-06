from datetime import datetime
from sqlalchemy import or_, select, update, delete, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List, Optional

from DAO.general_dao import GeneralDAO
from database import response_schemas
from database import models
from helpers import exception_helper
from services.user_services import UserService


class UserDAO:
    """
    Data Access Object for User model.
    Contains user-specific database operations.
    """
    @classmethod
    async def get_user_email(cls, 
                             db: AsyncSession, 
                             user_email: str) -> Optional[models.User]:
        """
        Find user by email address.
        
        :param db: Database session
        :param user_email: Email to search for
        :return: User object or None
        """
        query = select(models.User).where(models.User.email == str(user_email))
        email = await db.execute(query)

        return email.scalars().first()

    @classmethod
    async def get_user_name(cls, 
                            db: AsyncSession, 
                            user_name: str) -> Optional[models.User]:
        """
        Find user by username.
        
        :param db: Database session
        :param user_name: Username to search for
        :return: User object or None
        """
        query = select(models.User).where(models.User.name == str(user_name))
        name = await db.execute(query)

        return name.scalars().first()

    @classmethod
    async def get_user_by_id(cls, 
                             db: AsyncSession, 
                             user_id: int) -> Optional[models.User]:
        """
        Find user by ID.
        
        :param db: Database session
        :param user_id: User ID to find
        :return: User object or None
        """
        query = select(models.User).where(models.User.id == user_id)
        result = await db.execute(query)

        user = result.scalars().first()

        return user

    
    @classmethod
    async def get_user_with_posts(cls, 
                                  user_id: int,
                                  db: AsyncSession) -> response_schemas.UserWithPostsResponse:
        """
            Find user with posts by user's ID.
            
            :param db: Database session
            :param user_id: User ID to find
            :return: User data
        """
        user = await cls.get_user_by_id(user_id=user_id, db=db)
        await exception_helper.CheckHTTP404NotFound(founding_item=user, text="User not found")
        
        user_with_posts = await UserService.create_user_with_posts_response(user=user)

        return user_with_posts
    
    @classmethod
    async def get_all_users(cls,
                            db: AsyncSession) -> response_schemas.UserResponse:
        """
        Get all users from database and return formatted response.
        Delegates formatting to UserService.
        
        :param db: Database session
        :return: List[response_schemas.UserResponse] - List of formatted user responses
        """

        # Get all users from DB
        # users = await GeneralDAO.get_all_records(db=db, model=models.User)
        query = select(models.User).where(
            or_(
                models.User.is_active == True,
                models.User.is_active == 1,
                models.User.is_active == "true" # SQLite use this, so I add it here and also I add default "True" value
            )                                   # If u use Postgre mb it's should work too, cause I add "True" but "должно, но не обязано"
        )  

        result = await db.execute(query)

        users = result.scalars().all()
        await exception_helper.CheckHTTP404NotFound(founding_item=users, text="Users not found")
        
        # Delegate formatting to UserService to separate concerns
        users_list = await UserService.get_formated_users(users=users)

        return users_list
    
    @classmethod
    async def soft_delete_acc(cls,
                              user_id: int,
                              db: AsyncSession,
                              deleted_by_admin: bool = False,
                              deletion_reason: Optional[str] = '') -> models.User:
        
        query = select(models.User).where(models.User.id == user_id)

        result = await db.execute(query)

        user = result.scalars().first()
        await exception_helper.CheckHTTP404NotFound(founding_item=user, text="User not found or already deleted")

        user.is_active = False
        user.deleted_by_admin = deleted_by_admin
        user.deletion_reason = deletion_reason
        user.deleted_at = datetime.utcnow()

        await db.commit()
        await db.refresh(user)

    @classmethod
    async def soft_delete_user_posts(cls,
                                     db: AsyncSession,
                                     user_id: int) -> int:
        """
        Soft delete all posts of a user.
        Actually deletes them (hard delete) as requested.
        
        :param db: Database session
        :param user_id: ID of user whose posts to delete
        :return: Number of deleted posts
        """
        from DAO.post_dao import PostDao
        
        posts = await PostDao.get_posts_by_user_id(db=db, user_id=user_id)
        
        delete_count = 0
        for post in posts:
            await db.delete(post)
            delete_count += 1
        
        await db.commit()
        
        return delete_count
    
    @classmethod
    async def get_deleted_users(cls,
                                db: AsyncSession) -> list[models.User]:
        """
        Get all deleted users.
        
        :param db: Database session
        :return: List of deleted users
        """
        query = select(models.User).where(or_(
            models.User.is_active == False,
            models.User.is_active == "false"
        )).order_by(models.User.deleted_at.desc())
        
        result = await db.execute(query)
        return result.scalars().all()