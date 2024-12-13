from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool
from sqlalchemy import (
    select,
    delete,
)

from core.config import settings


async_engine = create_async_engine(
    url=settings.db.url_sqlite if settings.use_sqlite else settings.db.url_postgres,
    echo=settings.db.ECHO,
    pool_pre_ping=True,
    poolclass=NullPool,
)

async_session_factory = async_sessionmaker(
    bind=async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


SessionDep = Annotated[AsyncSession, Depends(get_async_session)]
