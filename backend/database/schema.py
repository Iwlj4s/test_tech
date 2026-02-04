from pydantic import BaseModel, Field

from typing import Union, Optional

"""
Pydantic schemas for data validation and serialization.
Used for request/response data modeling.
"""

# PUBLIC SCHEMAS #
class Item(BaseModel):
    """Schema for item creation and validation"""
    name: Union[str, None] = Field(default=None, min_length=3, title="Item name")
    description: Optional[str] = Field(default=None, min_length=3, title="Item description")
    created_at: Union[str] = Field(default=None, title="Item creation timestamp")

class ItemUpdate(BaseModel):
    """Schema for update item """
    name: Optional[str] = None
    description: Optional[str] = None

class User(BaseModel):
    """Schema for user registration and validation"""
    name: Union[str, None] = Field(default=None, min_length=3, title="User name")
    email: Union[str, None] = Field(default=None, title="User's email")
    password: Union[str, None] = Field(default=None, min_length=4, title="User's password")
    bio: Optional[str] = Field(default=None, min_length=10, title="User's biography")
    created_at: Union[str] = Field(default=None, title="User creation timestamp")

class UserSignIn(BaseModel):
    """Schema for user login authentication"""
    email: Union[str, None] = Field(default=None, title="User's email")
    password: Union[str, None] = Field(default=None, min_length=4, title="User's password")

class UserUpdate(BaseModel):
    """Schema for update user"""
    name: Union[str, None] = Field(default=None, min_length=3, title="User name")
    email: Union[str, None] = Field(default=None, title="User's email")
    bio: Optional[str] = Field(default=None, min_length=10, title="User's biography")


# ADMIN SCHEMAS #
class AdminUserCreate(User):
    """Schema for admin creation (only for admins)"""
    is_admin: bool = Field(default=False, title="Is user admin?")

class AdminUserUpdate(UserUpdate):
    """Schema for admin updating user (only for admins)"""
    is_admin: Optional[bool] = Field(default=None, title="Is user admin?")


# Post schemas
class PostCreate(BaseModel):
    """Schema for post creation"""
    content: Optional[str] = Field(default=None, min_length=1, title="Post content")


class PostUpdate(BaseModel):
    """Schema for post update"""
    content: Optional[str] = None