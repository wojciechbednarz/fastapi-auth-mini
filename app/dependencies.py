from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db import get_session, User
from app.schemas import TokenData
from app.auth import extract_payload_from_access_token
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import jwt


CREDENTIALS_EXCEPTION = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_db(session: Annotated[AsyncSession, Depends(get_session)]):
    """Dependency to get the database"""
    try:
        yield session
    finally:
        pass


async def get_current_user(
        db: Annotated[AsyncSession, Depends(get_db)],
        payload: Annotated[dict, Depends(extract_payload_from_access_token)]):
    """Gets the current user from the database"""
    try:
        username = payload.get("sub")
        print("Token payload:", payload)
        if username is None:
            raise CREDENTIALS_EXCEPTION
        query = select(User).where(
            User.username == username, User.is_active == True)
        result = await db.execute(query)
        user = result.scalars().first()
        print("Queried user:", user)
        if user is None:
            raise CREDENTIALS_EXCEPTION
        return user
    except jwt.PyJWTError:
        raise CREDENTIALS_EXCEPTION


async def get_current_active_user(
        current_user: Annotated[User, Depends(get_current_user)]
        ) -> User | None:
    """Gets the active user from the database"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
