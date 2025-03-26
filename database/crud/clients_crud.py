from asyncio.log import logger

from sqlalchemy.orm import selectinload

from ..engine import connection
from ..models import Client
from sqlalchemy import select
from typing import List, Dict, Any, Optional
from sqlalchemy.exc import SQLAlchemyError

@connection
async def create_client(session, data: dict, tg_id: int) -> Optional[Client]:
    try:
        client = await session.scalar(select(Client).where(Client.user_id == tg_id))

        if not client:
            new_client = Client(
                user_id=tg_id,
                name=data['name'],
                lastname=data['lastname'],
                number=data['number']
            )
            session.add(new_client)
            await session.commit()
            logger.info(f"Зарегистрировал пользователя с ID {tg_id}!")
            return None
        else:
            logger.info(f"Профиль с ID {tg_id} найден!")
    except SQLAlchemyError as e:
        logger.error(f"Ошибка при добавлении пользователя: {e}")
        # await session.rollback()

@connection
async def get_client(session, tg_id: int):
    result = await session.execute(
        select(Client).where(Client.user_id == tg_id)
    )

    client = result.scalars()
    return client

@connection
async def get_clients(session):
    clients = await session.scalars(select(Client))
    await session.commit()
    return clients

@connection
async def update_client(session, data: dict):
    client = await session.scalar(select(Client).where(Client.id == data['tg_id']))
    if client:
        client.name = data['name']
        client.lastname = data['lastname']
        client.number = data['number']
        await session.commit()

@connection
async def delete_client(session, tg_id: int):
    client = await session.scalar(select(Client).where(Client.user_id == tg_id))
    if client:
        await session.delete(client)
        await session.commit()
