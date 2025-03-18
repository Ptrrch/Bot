from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from asyncio.log import logger
from ..models import Admin
from ..engine import connection

@connection
async def create_admin(session, data: dict, tg_id: int):
    try:
        admin = await session.scalar(select(Admin).where(Admin.user_id == tg_id))

        if not admin:
            new_admin = Admin(
                user_id = tg_id,
                name = data['name'],
                lastname=data['lastname'],
                number = data['number']
            )
            session.add(new_admin)
            await session.commit()
        else:
            logger.info(f"Профиль с ID {tg_id} найден!")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        await session.rollback()


@connection
async def get_admin(session, tg_id: int):
    try:
        admin = await session.scalar(select(Admin).where(Admin.user_id == tg_id))
        if admin:
            return admin
        logger.info(f"Администратор с ID {tg_id} не найден!")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при поиске администратора: {e}")
        await session.rollback()


@connection
async def update_admin(session, data: dict, tg_id: int):
    try:
        admin = await session.scalar(select(Admin).where(Admin.user_id == tg_id))
        if admin:
            admin.name = data['name']
            admin.lastname = data['lastname']
            admin.number = data['number']
            await session.commit()
        else:
            logger.info(f"Администратор с ID {tg_id} не найден!")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при изменении администратора с ID {tg_id}: {e}")
        await session.rollback()


@connection
async def delete_admin(session, tg_id: int):
    try:
        admin = await session.scalar(select(Admin).where(Admin.user_id == tg_id))
        if admin:
            logger.info(f"Объект администратора перед удалением: {admin}")
            await session.delete(admin)  # Не забудьте использовать await
            await session.commit()
            logger.info(f"Администратор с ID {tg_id} успешно удален.")
        else:
            logger.info(f"Администратор с ID {tg_id} не найден!")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении администратора с ID {tg_id}: {e}")
        await session.rollback()


