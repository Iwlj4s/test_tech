from sqlalchemy import select, update, delete, and_, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from DAO.general_dao import GeneralDAO
from database import response_schemas, schema
from database import models
from helpers import exception_helper
from services.post_services import PostService


class PostDao:
    """
    Data Access Object for Post model.
    Contains post-specific database operations.
    """
    @classmethod
    async def create_post(cls, 
                          db: AsyncSession, 
                          request: schema.PostCreate, 
                          user_id: int) -> models.Post:
        """
        Create new post in database.
        
        :param db: Database session
        :param request: Post data from schema
        :param user_id: ID of user creating the post
        :return: Created post object
        """

        content = request.content or ""
        new_post = models.Post(
            content=content,
            user_id=user_id
        )

        db.add(new_post)
        await db.commit()
        await db.refresh(new_post)

        return new_post
    
    @classmethod
    async def update_post(cls,
                          post_id: int,
                          user_id: int,
                          post_data: schema.PostUpdate,
                          db: AsyncSession) -> models.Post:
        
        post = await cls.get_post_by_user_id(db=db, 
                                            post_id=post_id, 
                                            user_id=user_id)
        await exception_helper.CheckHTTP404NotFound(founding_item=post, 
                                              text="Post not found or you don't have permission to update it")
        update_data = post_data.dict(exclude_unset=True)
        for k, v in update_data.items():
            setattr(post, k, v)

        await db.commit()
        await db.refresh(post)

        return post
    
    @classmethod
    async def delete_post(cls,
                          post_id: int,
                          user_id: int,
                          db: AsyncSession) -> None:

        """
        Delete post with ownership verification.
        Only post owner can delete their posts.
        
        :param db: Database session
        :param post_id: ID of post to delete
        :param user_id: User ID for ownership verification
        """
        query = delete(models.Post).where(
            and_(
                models.Post.id == post_id,
                models.Post.user_id == user_id
            )
        )

        await db.execute(query)

        await db.commit()

    @classmethod
    async def get_posts_by_user_id(cls, 
                                   db: AsyncSession, 
                                   user_id: int) -> List[models.Post]:
        """
        Get all posts belonging to specific user.
        
        :param db: Database session
        :param user_id: User ID to filter posts
        :return: List of user's posts
        """
        query = select(models.Post).where(models.Post.user_id == user_id)
        posts = await db.execute(query)
        return posts.scalars().all()

    @classmethod
    async def get_post_by_user_id(cls, db: AsyncSession,
                                  post_id: int,
                                  user_id: int) -> Optional[models.Post]:
        """
        Get specific post with ownership verification.
        
        :param db: Database session
        :param post_id: Post ID to find
        :param user_id: User ID for ownership check
        :return: Post object or None
        """
        query = select(models.Post).where(
            and_(
                models.Post.user_id == user_id,
                models.Post.id == post_id
            )
        )
        post = await db.execute(query)
        return post.scalars().first()
    
    @classmethod
    async def get_all_posts(cls,
                            db: AsyncSession) -> response_schemas.PostResponse:
        """
        Get all posts from database with associated user information.
        Delegates response formatting to PostService.
        
        :param db: Database session
        :return: List[response_schemas.PostWithUserResponse] - Formatted posts with user data
        """

        # Get all Posts from DB
        posts = await GeneralDAO.get_all_records(db=db, model=models.Post)
        await exception_helper.CheckHTTP404NotFound(founding_item=posts, text="Posts not found")

        # Delegate formatting to PostService to separate concerns
        posts_list = await PostService.get_formated_posts(items=posts)
        return posts_list
