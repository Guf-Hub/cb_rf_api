import logging

from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.db.models.base import Base
from api_v1.db.session import async_engine, delete, SessionDep


async def async_create_db():
    try:
        async with async_engine.begin() as conn:
            async_engine.echo = False
            await conn.run_sync(Base.metadata.create_all)
            async_engine.echo = False
            logging.info("Database created successfully: %s", async_engine.url)
    except Exception as e:
        logging.error("Create database error: %s", e, exc_info=True)
        logging.error("Database connection string: %s", async_engine.url)


async def async_drop_db():
    try:
        async with async_engine.begin() as conn:
            async_engine.echo = False
            await conn.run_sync(Base.metadata.drop_all)
            # async_engine.echo = True
    except Exception as e:
        logging.error("Drop database error: %s", e, exc_info=True)


async def truncate_table(table, session: AsyncSession = SessionDep):
    try:
        async with session.begin():
            await session.execute(delete(table))
            await session.commit()
            logging.info("Truncated table: %s", table.__tablename__)
    except Exception as e:
        logging.error("Truncate table error: %s", e)
