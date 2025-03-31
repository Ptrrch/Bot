from sqlalchemy import select
from asyncio.log import logger

from sqlalchemy.exc import SQLAlchemyError

from database.models import User
from database.engine import connection


@connection
async def create_user(session, tg_id:int):
    try:
        user = await session.scalar(select(User).where(User.user_id == tg_id))
        if not user:
            new_user = User(
                user_id = tg_id
            )
            session.add(new_user)
            await session.commit()
            logger.info(f"{tg_id} Успешно добавлен в базу данных")
        else:
            logger.info(f"{tg_id} уже есть в базе данных!")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении города: {e}")
        await session.rollback()

@connection
async def get_user_id(session, user_id: int) -> int:
    try:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        if user:
            return user.id
        else:
            logger.info("")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при поиске города: {e}")
        await session.rollback()

@connection
async def get_user_tg_id(session, id: int) -> int:
    try:
        user = await session.scalar(select(User).where(User.id == id))
        if user:
            return user.user_id
        else:
            logger.info("")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при поиске города: {e}")
        await session.rollback()







