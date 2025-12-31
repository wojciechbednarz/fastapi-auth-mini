""""Learning app to get to know better concepts of:
- Authentication
- Password hashing
- JWT access tokens
- Token expiration
- Token verification
- Auth dependency for protected routes 
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from app.auth import hash_password, create_access_token, verify_password, ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import datetime, timezone, timedelta
from app.schemas import UserCreate, UserResponse
from app.dependencies import get_db, get_current_active_user
from app.models import User
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.db import create_db_and_tables
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan function to create database and tables on startup"""
    await create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)



@app.get("/")
async def root():
    """API root endpoint"""
    return {"message": "Root endpoint"}


@app.get("/health")
async def health_check():
    """API endpoint to check health status of the app"""
    return {"message": "API is runnning"}


@app.get("/users/me")
async def read_users_me(user: Annotated[User, Depends(get_current_active_user)]):
    """Read current user"""
    return user


@app.post("/auth/register")
async def user_register(
    user: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)]) -> UserResponse:
    """API endpoint which creates a user"""
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        created_at=datetime.now(timezone.utc)
        )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user



@app.post("/auth/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """API endpoint to login"""
    query = select(User).where(User.username == form_data.username)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(payload={"sub": user.username},
                                       expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
