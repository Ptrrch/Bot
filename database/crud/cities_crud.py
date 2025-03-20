from sqlalchemy import select
from asyncio.log import logger

from sqlalchemy.exc import SQLAlchemyError

from database.models import City
from database.engine import connection


@connection
async def create_city(session, data: dict):
    try:
        city = await session.scalar(select(City).where(City.title == data['title']))
        if not city:
            new_city = City(
                title = data['title']
            )
            session.add(new_city)
            await session.commit()
            logger.info(f"{data['title']} Успешно добавлен в базу данных")
        else:
            logger.info(f"{data['title']} уже есть в базе данных!")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении города: {e}")
        # await session.rollback()

@connection
async def get_city(session):
    try:
        city = await session.scalars(select(City))
        return city

        logger.info("В базе данных пока еще нет городов")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при поиске города: {e}")
        # await session.rollback()

@connection
async def get_one_city(session, id:int):
    try:
        city = await session.scalar(select(City).where(City.id == id))
        return city

        logger.info("В базе данных пока еще нет городов")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при поиске города: {e}")
        # await session.rollback()



@connection
async def update_city(session, data: dict):
    try:
        city = await session.scalar(select(City).where(City.id == data['id']))
        if city:
            city.title = data['tittle']
            await session.commit()
            logger.info(f"Город {id} успешно обновлен")
        logger.info(f"Города под номер {id} еще нет в базе данных")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при обновлении города: {e}")
        # await session.rollback()


@connection
async def delete_city(session, data: dict):
    try:
        city = await session.scalar(select(City).where(City.id == data['id']))
        if city:
            await session.delete(city)
            await session.commit()
            logger.info(f"Город {id} успешно удален")
        logger.info(f"Города под номер {id} еще нет в базе данных")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении города: {e}")
        # await session.rollback()
