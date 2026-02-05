from fastapi import Depends, APIRouter, Response
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List


from DAO.user_dao import UserDAO
from context.request_context import RequestContext, get_request_context
from database import response_schemas, schema
from database.database import get_db

from repository import post_repository
from repository.user_repository import get_current_user


post_router = APIRouter(
    prefix="/posts",
    tags=["post_router"]
)


@post_router.get("/")
async def get_posts_list(db: AsyncSession = Depends(get_db)) -> response_schemas.PostListResponse:
    posts_list = await post_repository.get_all_posts(db=db)
    return posts_list


@post_router.get("/post/{post_id}")
async def get_post(post_id: int,
                   db: AsyncSession = Depends(get_db)) -> response_schemas.PostDetailResponse:
    return await post_repository.show_post(post_id=int(post_id),
                                           db=db)

@post_router.get("/{user_id}/posts")
async def get_user_posts(user_id: int,
                         db: AsyncSession = Depends(get_db)) -> response_schemas.UserWithPostsDataResponse:

    return await post_repository.get_user_with_posts(user_id=user_id, db=db)

@post_router.post("/create_post")
async def add_post(request: schema.PostCreate,
                   request_context: RequestContext = Depends(get_request_context)) -> response_schemas.PostCreateResponse:
    return await post_repository.create_post(request=request,
                                             current_user=request_context.current_user, 
                                             db=request_context.db)


@post_router.patch("/update_post/{post_id}", status_code=200)
async def update_post(post_id: int,
                      post_data: schema.PostUpdate,
                      request_context: RequestContext = Depends(get_request_context)) -> response_schemas.PostUpdateResponse:
    return await post_repository.update_post(post_id=post_id,
                                             user_id=request_context.current_user.id,
                                             post_data=post_data,
                                             db=request_context.db)


@post_router.delete("/delete_post/{post_id}")
async def delete_post(post_id: int,
                      request_context: RequestContext = Depends(get_request_context)) -> response_schemas.PostDeleteResponse:
    return await post_repository.delete_post(post_id=post_id, 
                                             user_id=request_context.current_user.id,
                                             db=request_context.db)
