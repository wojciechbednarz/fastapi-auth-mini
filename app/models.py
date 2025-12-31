# models.py
from sqlmodel import Field, SQLModel
from datetime import datetime, timezone

class User(SQLModel, table=True):
    """SQLModel model for User"""
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True, index=True)
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=timezone.utc, nullable=False)
    is_active: bool = Field(default=True, nullable=False)