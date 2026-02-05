from typing import List
from datetime import datetime
from sqlalchemy import String, ForeignKey, Column, Integer, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from database.database import Base


class User(Base):
    """
    System user model.
    Contains basic information and relationship with user's items.
    """
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, unique=True)  # Unique username
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False) # Unique email
    password: Mapped[str] = mapped_column(String)    # Hashed password
    
    bio: Mapped[str] = mapped_column(String,        # User's biography 
                                     nullable=False,
                                     server_default="User didn't add his bio")
    
    location: Mapped[str] = mapped_column(String,   # User's location. Like Miami/Hamburg
                                          nullable=True,
                                          server_default="")
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),   # Creation timestamp
                                                 nullable=False,
                                                 server_default=func.now())
    
    is_admin: Mapped[bool] = mapped_column(Boolean, # Is User admin? True/False
                                           nullable=False,
                                           server_default="false")
    
    is_active: Mapped[bool] = mapped_column(Boolean,    # Active/Deleted flag
                                            nullable=False,
                                            server_default="true")
    deleted_by_admin: Mapped[bool] = mapped_column(Boolean,    # Who deleted account? 
                                                   nullable=False,
                                                   server_default="false")
    deletion_reason: Mapped[str] = mapped_column(String,    # Who deleted account? 
                                                 nullable=True,
                                                 server_default=None)
    deleted_at: Mapped[str] = mapped_column(DateTime(timezone=True),    # When deleted
                                            nullable=True,
                                            default=None)
    
    # One-to-many relationship with Post model
    posts: Mapped[List["Post"]] = relationship(
        "Post",
        back_populates="user",
        lazy="selectin"
    )


class Post(Base):
    """
    Post model for user-generated posts (e.g., tweets)
    """
    __tablename__ = 'posts'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    content: Mapped[str] = mapped_column(String,
                                         nullable=False,
                                         server_default="")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now())
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    user: Mapped["User"] = relationship(
        "User",
        back_populates="posts",
        lazy="selectin"
    )