from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from database import models
from database import response_schemas

class PostService:
    """
    Service layer for post-related business logic and response formatting.
    """

    @staticmethod
    async def get_formated_posts(items: List) -> response_schemas.PostResponse:
        """
        Transform list of SQLAlchemy Post models into API response format.
        """

        posts_list = []
        for item in items:
            item_data = response_schemas.PostWithUserResponse(
                id=item.id,
                content=item.content,
                created_at=item.created_at,
                user_id=item.user.id,
                user_name=item.user.name,
                user_email=item.user.email
            )
            posts_list.append(item_data)

        return posts_list
    
    @staticmethod
    async def create_post_detail_response(post: models.Post) -> response_schemas.PostDetailResponse:
        return response_schemas.PostWithUserResponse(
            id=post.id,
            content=post.content,
            created_at=post.created_at,
            user_id=post.user_id,
            user_name=post.user.name,
            user_email=post.user.email
        )
