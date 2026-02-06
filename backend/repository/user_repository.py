from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any, List

from starlette import status
from starlette.responses import Response

from DAO.post_dao import PostDao
from services.post_services import PostService
from services.user_services import UserService
from database.database import get_db
from database import models, schema, response_schemas

from helpers import password_helper, user_helper
from helpers import exception_helper
from helpers.exception_helper import CheckHTTP404NotFound, CheckHTTP409Conflict, CheckHTTP403FORBIDDEN_BOOL
from helpers.token_helper import get_token, verify_token

from DAO.general_dao import GeneralDAO
from DAO.user_dao import UserDAO

from helpers import password_helper


"""
User business logic layer.
Handles user authentication, registration, and user-related operations.
"""


async def sign_up(request: schema.User,
                  db: AsyncSession) -> response_schemas.UserCreateResponse:
    
    """
    Register a new user in the system.
    Validates email and username uniqueness.
    
    :param request: User registration data
    :param db: Database session

    :return: Success response with user data or error
    :raises HTTPException: 409 if email or username already exists
    """
    # Check for existing email
    email = await UserDAO.get_user_email(db=db, user_email=str(request.email))
    # Check for existing username
    name = await UserDAO.get_user_name(db=db, user_name=str(request.name))

    # Return conflict error if email exists
    await CheckHTTP409Conflict(email, "Email already exists")

    # Return conflict error if username exists
    await CheckHTTP409Conflict(name, "This username already exists")

    print(f"   Original password from request: '{request.password}'")
    print(f"   Password length: {len(request.password)}")
    print(f"   Password type: {type(request.password)}")

    # Hash password and create new user
    hash_password = password_helper.hash_password(request.password)
    print(f"   Hashed password: {hash_password}")
    print(f"   Hashed password length: {len(hash_password)}")

    new_user = models.User(name=request.name, 
                           email=request.email, 
                           password=hash_password,
                           bio=request.bio,
                           location=request.location,
                           is_admin=False,
                           deleted_by_admin=False)
    db.add(new_user)

    await db.commit()
    await db.refresh(new_user)
    print(f"   User created with ID: {new_user.id}")

    user_data = await UserService.create_user_response(user=new_user)

    return response_schemas.UserCreateResponse(
        message="User has been created successfully",
        status_code=200,
        data=user_data
    )


async def login(request: schema.UserSignIn,
                response: Response,
                db: AsyncSession) -> response_schemas.UserLoginResponse:
    """
    Authenticate user and generate access token.
    
    :param request: User login credentials
    :param response: HTTP response object
    :param db: Database session

    :return: User data with access token or error
    """
    user = await user_helper.take_access_token_for_user(db=db,
                                                        response=response,
                                                        request=request)
    # Return error if authentication failed
    if response.status_code == status.HTTP_403_FORBIDDEN:
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': "FORBIDDEN"
        }

    return response_schemas.UserLoginResponse(
        message="Login successful",
        status_code=200,
        data=user
    )

async def get_current_user(db: AsyncSession = Depends(get_db),
                           token: str = Depends(get_token)) -> response_schemas.UserResponse:
    """
    Get current authenticated user from JWT token.
    Used as dependency in protected routes.
    
    :param db: Database session
    :param token: JWT token from request

    :return: User object or error response
    :raises HTTPException: 401 if token invalid or user not found
    """
    user_id = verify_token(token=token)
    print("user_id in get current user: ", user_id)
    if not user_id:
        return {
            'message': "Token not found",
            'status_code': 401,
        }
    user = await GeneralDAO.get_record_by_id(record_id=user_id,
                                             model=models.User, 
                                             db=db)
    
    if not user or not user.is_active:        
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Account is deleted",
            headers={"WWW-Authenticate": "Bearer"})
    
    user_data = await UserService.create_user_response(user=user)

    return user_data


async def update_me(user_id: int,
                    user_data: schema.UserUpdate,
                    current_user: schema.User,
                    db: AsyncSession) -> response_schemas.UserUpdateResponse:
    """
    Update current authenticated user's profile.        

    :param user_id: ID of the user to update
    :param user_data: Data to update
    :param current_user: Authenticated user
    :param db: Database session

    :return: Updated user data
    :raises HTTPException: 404 if user not found or 403 if updating another user's profile
    """

    await CheckHTTP403FORBIDDEN_BOOL(condition=(user_id != current_user.id),
                                    text="You can update only your own profile")
    
    if not user_data.dict(exclude_unset=True):
        raise HTTPException(status_code=400, detail="No fields for update")
    
    updating_user = await GeneralDAO.get_record_by_id(record_id=user_id,
                                                      model=models.User,
                                                      db=db)
    
    await CheckHTTP404NotFound(founding_item=updating_user, text="User not found")

    if "is_admin" in user_data:
        # Only admin can change "is admin" field
        if not current_user or not current_user.is_admin:
            raise HTTPException(
                status_code=403,
                detail="Only administrators can change user roles"
            )

    updated_user = await GeneralDAO.update_record(model=models.User,
                                                  record=updating_user,
                                                  update_data=user_data,
                                                  db=db)
    
    user_data = await UserService.create_user_response(user=updated_user)

    return response_schemas.UserUpdateResponse(
        message="User has been updated",
        status_code=200,
        data = user_data
    )

async def get_current_user_posts(current_user: schema.User, 
                                 db: AsyncSession = Depends(get_db)) -> response_schemas.UserWithPostsDataResponse:
    """
    Get all items belonging to the current authenticated user.
    
    :param current_user: Authenticated user
    :param db: Database session

    :return: User's items
    :raises HTTPException: 404 if no items found
    """
    items = await PostDao.get_posts_by_user_id(db=db, user_id=current_user.id)
    await CheckHTTP404NotFound(items, "No posts found for this user")

    # Use Response Schema to avoid recursion
    user_data = await UserDAO.get_user_with_posts(user_id=current_user.id, db=db)
    #user_with_posts = await UserService.create_user_with_posts_response(user=current_user)

    return response_schemas.UserWithPostsDataResponse(
        message="User posts retrieved successfully",
        status_code=200,
        data=user_data
    )

async def get_current_user_post(post_id: int,
                                current_user: schema.User,
                                db: AsyncSession = Depends(get_db)) -> response_schemas.PostDetailResponse:
    """
    Get specific item belonging to the current user.
    
    :param item_id: ID of item to retrieve
    :param current_user: Authenticated user
    :param db: Database session

    :return: User's specific item
    :raises HTTPException: 404 if item not found or doesn't belong to user
    """
    
    post = await PostDao.get_post_by_user_id(db=db, 
                                             user_id=current_user.id, 
                                             post_id=post_id)
    
    await CheckHTTP404NotFound(founding_item=post, text="Post not found")
    
    post_data = await PostService.create_post_detail_response(post=post)

    return response_schemas.PostDetailResponse(
        message="Post retrieved successfully",
        status_code=200,
        data=post_data 
    )


async def get_all_users(db: AsyncSession) -> response_schemas.UserListResponse:
    """
    Retrieve all users from the system with their items.
    
    :param db: Database session
    :return: List of all users with their items
    :raises HTTPException: 404 if no users found
    """
    users = await UserDAO.get_all_users(db=db)
    
    return response_schemas.UserListResponse(
        message="Users retrieved successfully",
        status_code=200,
        data=users
    )

async def delete_current_user(current_user: models.User,
                              db: AsyncSession) -> response_schemas.UserDeleteResponse:
    """
    User deletes their own account.
    
    :param current_user: Authenticated user
    :param db: Database session
    :return: Deletion response
    """
    # Check if user is already deleted
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account is already deleted"
        )
    
    # Soft delete user
    deleted_user = await UserDAO.soft_delete_acc(db=db,
                                                 user_id=current_user.id,
                                                 deleted_by_admin=False,
                                                 deletion_reason=None)
    
    # Delete user's posts (hard delete)
    deleted_posts_count = await UserDAO.soft_delete_user_posts(db=db,
                                                               user_id=current_user.id)
    
    return response_schemas.UserDeleteResponse(
        message=f"Your account has been deleted successfully. {deleted_posts_count} posts removed.",
        status_code=200)