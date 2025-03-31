from itertools import count

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database.crud.cities_crud import create_city, get_city, get_one_city
from database.engine import connection
from database.models import Kitchen, City
#
@connection
async def create_kitchen(session, data: dict) -> None:
    kitchen = await session.scalar(select(Kitchen).where(Kitchen.user_id == data['user_id']))
    if not kitchen:
        kitchen = Kitchen(
            user_id=data['user_id'],
            title=data['title'],
            description=data['description'],
            address=data['address'],
            number=data['number'],
            city_id=data['city_id']
        )
        session.add(kitchen)
        await session.commit()
    else:
        print("Кухня для этого пользователя уже существует")


@connection
async def append_city_to_kitchen(session, tg_id: int, city_id: int) -> None:
    try:
        city = await session.scalar(
            select(City)
            .options(selectinload(City.kitchens))
            .where(City.id == city_id)
        )
        kitchen = await session.scalar(select(Kitchen).where(Kitchen.id == tg_id))
        city.kitchens.append(kitchen)


        await session.commit()
    except Exception as e:
        print(f"An error occurred while adding cities to kitchen: {e}")
        await session.rollback()


@connection
async def get_kitchen(session, id: int) -> Kitchen | None:
    kitchen = await session.scalar(
        select(Kitchen)
        .options(selectinload(Kitchen.cities))
        .where(Kitchen.id == id)
    )
    return kitchen




@connection
async def get_kitchens(session) -> list[Kitchen] | None:
    kitchens = await session.scalars(
        select(Kitchen)
    )
    return kitchens


@connection
async def update_kitchen(session, data: dict) -> None:
    kitchen = await session.scalar(select(Kitchen).where(Kitchen.id == data['id']))
    if kitchen:
        kitchen.title=data['title']
        kitchen.description=data['description']
        kitchen.address=data['address']
        kitchen.number=data['number']
    await session.commit()


@connection
async def delete_kitchen(session, id: int) -> None:
    data = await session.scalar(select(Kitchen).where(Kitchen.id==id))
    if data:
        await session.delete(data)
        await session.commit()





