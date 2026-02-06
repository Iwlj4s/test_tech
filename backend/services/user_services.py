from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import models
from database import response_schemas

class UserService:
    """
    Service layer for user-related business logic and response formatting.
    Contains operations that transform database models into API response schemas.
    """

    @staticmethod
    async def get_formated_users(users: List) -> response_schemas.UserResponse:
        """
        Transform list of SQLAlchemy User models into API response format.
        
        :param users: List[models.User] - List of User database models

        :return: List[response_schemas.UserResponse] - Formatted users ready for API response

        Note:
            Uses Pydantic schemas to avoid recursion and control response structure.
            Handles serialization and filtering of sensitive data.
        """

        users_list = []
        for user in users:
            user_data = response_schemas.UserResponse(
                id=user.id,
                name=user.name,
                email=user.email,
                bio=user.bio,
                location=user.location,
                created_at=user.created_at,
                is_admin=user.is_admin,
                is_active=user.is_active,
                deleted_by_admin=user.deleted_by_admin,
                deletion_reason=user.deletion_reason,  
                deleted_at=user.deleted_at,                       
            )
            users_list.append(user_data)

        return users_list
    
    @staticmethod
    async def create_user_response(user: models.User) -> response_schemas.UserResponse:
        """Creating UserResponse from SQLAlchemy User model"""

        return response_schemas.UserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
            bio=user.bio or "",
            location=user.location or "",
            created_at=user.created_at,
            is_admin=user.is_admin,
            is_active=user.is_active,
            deleted_by_admin=user.deleted_by_admin,
            deletion_reason=user.deletion_reason,
            deleted_at=user.deleted_at
    )
    
    @staticmethod
    async def create_user_with_posts_response(user: models.User) -> response_schemas.UserWithPostsResponse:
        user_data = await UserService.create_user_response(user=user)
        posts = [
             response_schemas.PostResponse(
                id=post.id,
                content=post.content,
                created_at=post.created_at,
                user_id=post.user_id
            )
            for post in user.posts
        ]

        return response_schemas.UserWithPostsResponse(
            **user_data.dict(),  # Transform to dict cause UserWithPostsResponse wait named args for fields
            posts=posts
        )