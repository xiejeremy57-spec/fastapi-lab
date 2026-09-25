from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker
)
from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import DeclarativeBase


DATABASE_URL = "sqlite+aiosqlite:///./fastapi_lab.db"


# 数据库引擎
engine = create_async_engine(
    DATABASE_URL,
    echo=True
)


# 创建 Session 工厂
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


# ORM 基类
class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncIterator[AsyncSession]:

    async with AsyncSessionLocal() as session:
        yield session