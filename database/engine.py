from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine, async_session

from .models import Base
from .config import settings


engine = create_async_engine(settings.db_url, echo=settings.db_echo)
session_maker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)



def connection(func):
    async def wrapper(*args, **kwargs):
        async with session_maker() as session:
            return await func(session, *args, **kwargs)

    return wrapper

def connection_call(func):
    async def wrapper(call: CallbackQuery, state: FSMContext, *args, **kwargs):
        async with session_maker() as session:
            return await func(call, state, session, *args, **kwargs)
    return wrapper


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

