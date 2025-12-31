from sqlmodel import Session, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from typing import AsyncGenerator
from app.models import User


DATABASE_URL = "sqlite+aiosqlite:///./test.db"


engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    )

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def create_db_and_tables():
    """Create database and tables"""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency to get DB session"""
    async with async_session_maker() as session:
        yield session
