import asyncio
import os
import aiosqlite
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, async_session

from .models import Base

#from .env file:
DB_LITE="sqlite+aiosqlite:///my_base.db"
# DB_URL=postgresql+asyncpg://login:password@localhost:5432/db_name

# engine = create_async_engine(os.getenv('DB_LITE'), echo=True)

engine = create_async_engine("sqlite+aiosqlite:///database/my_base.db", echo=True)

session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



def connection(func):
    async def wrapper(*args, **kwargs):
        async with session_maker() as session:
            return await func(session, *args, **kwargs)

    return wrapper


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

