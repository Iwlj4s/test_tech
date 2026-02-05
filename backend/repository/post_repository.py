from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List


from starlette.responses import Response

from DAO.user_dao import UserDAO
from database import schema, models, response_schemas

from helpers import exception_helper
from DAO.general_dao import GeneralDAO
from DAO.post_dao import PostDao
from database.database import get_db


async def create_post(request: schema.PostCreate,
                      current_user: schema.User,
                      db: AsyncSession = Depends(get_db)) -> response_schemas.PostCreateResponse:
    """
    Create a new post for the current user.
    """
    new_post = await PostDao.create_post(db=db,
                                         request=request,
                                         user_id=current_user.id)

    return response_schemas.PostCreateResponse(
        message="Post has been created successfully",
        status_code=200,
        data=response_schemas.PostResponse(
            id=new_post.id,
            content=new_post.content,
            created_at=new_post.created_at,
            user_id=new_post.user_id
        )
    )


async def update_post(post_id: int,
                      user_id: int,
                      post_data: schema.PostUpdate,
                      db: AsyncSession) -> response_schemas.PostUpdateResponse:

    if not post_data.dict(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No fields to update")
    
    post = await PostDao.get_post_by_user_id(db=db, 
                                            post_id=post_id, 
                                            user_id=user_id)
    
    await exception_helper.CheckHTTP404NotFound(founding_item=post, 
                                              text="Post not found or you don't have permission to update it")
    
    updated_post = await GeneralDAO.update_record(model=models.Post,
                                                  record=post,
                                                  update_data=post_data,
                                                  db=db)
    
    return response_schemas.PostUpdateResponse(
        message="Post has been updated",
        status_code=200,
        data = response_schemas.PostResponse(
            id=updated_post.id,
            content=updated_post.content,
            created_at=updated_post.created_at,
            user_id=updated_post.user_id
        )
    )


async def delete_post(post_id: int,
                      user_id: int,
                      db: AsyncSession) -> response_schemas.PostDeleteResponse:

    post = await PostDao.get_post_by_user_id(db=db, 
                                             post_id=post_id, 
                                             user_id=user_id)
    await exception_helper.CheckHTTP404NotFound(founding_item=post, 
                                              text="Post not found or you don't have permission to delete it")

    await PostDao.delete_post(db=db, post_id=post_id, user_id=user_id)

    return response_schemas.PostDeleteResponse(
        message="Post has been deleted",
        status_code=200
    )


async def show_post(post_id: int,
                    db: AsyncSession = Depends(get_db)) -> response_schemas.PostDetailResponse:
    post = await GeneralDAO.get_record_by_id(record_id=post_id,
                                             model=models.Post,
                                             db=db)
    await exception_helper.CheckHTTP404NotFound(founding_item=post, text="Post not found")
    
    return response_schemas.PostDetailResponse(
        message="Post retrieved successfully",
        status_code=200,
        data=response_schemas.PostWithUserResponse(
            id=post.id,
            content=post.content,
            created_at=post.created_at,
            user_id=post.user.id,
            user_name=post.user.name,
            user_email=post.user.email
        )
    )


async def get_all_posts(db: AsyncSession) -> response_schemas.PostListResponse:

    posts_list = await PostDao.get_all_posts(db=db)
    
    return response_schemas.PostListResponse(
        message="Posts retrieved successfully",
        status_code=200,
        data=posts_list
    )

async def get_user_with_posts(user_id: int,
                              db: AsyncSession) -> response_schemas.UserWithPostsDataResponse:

    users_data = await UserDAO.get_user_with_posts(user_id=user_id,
                                                    db=db)
    
    return response_schemas.UserWithPostsDataResponse(
        message="User's poists retrieved successfully",
        status_code=200,
        data=users_data
    )