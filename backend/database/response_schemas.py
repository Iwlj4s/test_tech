from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional, Generic, TypeVar

# Type variable for generic types - represents any data type
T = TypeVar('T')

class BaseResponse(BaseModel):
    """
    Base schema for all API responses.
    Provides consistent structure for all endpoints.
    
    All API responses will have:
    - message: Human-readable result description
    - status_code: HTTP status code
    
    Example Response:
    -----------------
    {
        "message": "Operation completed successfully",
        "status_code": 200
    }
    """
    message: str
    status_code: int
    
    class Config:
        from_attributes = True


class DataResponse(BaseResponse, Generic[T]):
    """
    Generic response schema for single object endpoints.
    Extends BaseResponse with optional data field of any type.
    
    Usage:
    - Single object retrieval (GET /items/{id})
    - Create operations (POST /items)
    - Update operations (PATCH /items/{id})
    
    Generic type T determines the data structure:
    - DataResponse[ItemResponse] for item data
    - DataResponse[UserResponse] for user data
    
    Example Response:
    -----------------
    {
        "message": "Item retrieved successfully",
        "status_code": 200,
        "data": {
            "id": 1,
            "name": "Laptop",
            "description": "Gaming laptop",
            "user_id": 5
        }
    }
    """
    data: Optional[T] = None


class ListResponse(BaseResponse, Generic[T]):
    """
    Generic response schema for list/collection endpoints.
    Extends BaseResponse with data field containing list of objects.
    
    Usage:
    - List operations (GET /items)
    - Bulk operations returning multiple objects
    
    Generic type T determines the structure of list items:
    - ListResponse[ItemWithUserResponse] for items with user info
    - ListResponse[UserResponse] for basic user list
    
    Example Response:
    -----------------
    {
        "message": "Items retrieved successfully",
        "status_code": 200,
        "data": [
            {
                "id": 1,
                "name": "Laptop",
                "description": "Gaming laptop",
                "user_id": 5,
                "user_name": "John Doe",
                "user_email": "john@example.com"
            }
        ]
    }
    """
    data: List[T] = []


# Basic enity schemas (without relationships)
class UserResponse(BaseModel):
    """
    Basic user schema without relationships to avoid recursion.
    Contains essential user information for API responses.
    
    Fields:
    - id: Unique user identifier
    - name: User's display name
    - email: User's email address
    
    Use when you need user data without nested item information.
    """
    id: int
    name: str
    email: str
    bio: str
    location: str
    created_at: datetime
    is_admin: bool
    is_active: bool
    deleted_by_admin: Optional[bool] = None 
    deletion_reason: Optional[str] = None
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class CurrentUserResponse(UserResponse):
    """
    Basic item schema without relationships to avoid recursion.
    Contains essential item information for API responses.
    
    Fields:
    - user_access_token: User token for get current user
    
    Use when you need item data without nested user information.
    """
    user_access_token: str

class UserDeleteResponse(BaseResponse):
    """Response type for user deletion endpoints"""
    user_id: Optional[int] = None
    deletion_reason: Optional[str] = None

class PostResponse(BaseModel):
    """
    Basic post schema without relationships.
    """
    id: int
    content: str
    created_at: datetime
    user_id: int

    class Config:
        from_attributes = True


# Composite schemas (with relationships)
class PostWithUserResponse(PostResponse):
    """
    Extended post schema including owner information.
    """
    user_name: str
    user_email: str

class UserWithPostsResponse(UserResponse):
    """
    Schema for user with posts (flattened structure).
    Prevents recursion by including items as basic ItemResponse objects.
    
    :param id:      int
                    Unique identifier of the user

    :param name:    str  
                    Full name of the user

    :param email:   str
                    Email address of the user

    :param posts:   List[PostResponse]
                    List of user's posts without nested user data to avoid recursion
    """

    posts: List[PostResponse] = []
    

# Response type aliases for better readability in route annotations
# Users
UserListResponse = ListResponse[UserResponse]  
"""Response type for get all users endpoints"""

UserCreateResponse = DataResponse[UserResponse]
"""Response type for user creation endpoints"""

UserUpdateResponse = DataResponse[UserResponse]
"""Response type for user update endpoints"""

UserLoginResponse = DataResponse[CurrentUserResponse]
"""Response type for get current user"""

UserWithPostsDataResponse = DataResponse[UserWithPostsResponse]
"""Response type for user retrieval with posts"""

# Posts
PostCreateResponse = DataResponse[PostResponse]
"""Response type for post creation endpoints"""

PostUpdateResponse = DataResponse[PostResponse]
"""Response type for post update endpoints"""

PostDeleteResponse = BaseResponse
"""Response type for post deletion endpoints"""

PostDetailResponse = DataResponse[PostWithUserResponse]
"""Response type for single post retrieval with user info"""

PostListResponse = ListResponse[PostWithUserResponse]
"""Response type for post list retrieval with user info"""