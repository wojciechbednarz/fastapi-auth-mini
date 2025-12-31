"""Pydantic schemas"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field



class UserBase(BaseModel):
    """Pydantic validation scheme for base user"""
    email: EmailStr
    username: str


class UserCreate(UserBase):
    """Pydantic validation scheme for user creation"""
    password:str = Field(
        ..., min_length=6, description="Password must be prvided by the user")


class UserResponse(UserBase):
    """Pydantic validation scheme for user response"""
    id: int
    is_active: bool
    created_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None

