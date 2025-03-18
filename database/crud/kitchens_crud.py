from sqlalchemy import select

from database.engine import connection
from database.models import Kitchen, City

@connection
async def create_kitchen(session, data: dict) -> None:
    kitchen = await session.scalar(select(Kitchen).where(Kitchen.user_id ==data['tg_id']))
    if not kitchen:
        kitchen = Kitchen(
            user_id=data['tg_id'],
            title=data['title'],
            description=data['description'],
            number=data['number']
        )
        session.add(kitchen)
        await session.commit()
    else:
        ...

@connection
async def append_city_to_kitchen(session, kitchen: Kitchen, data: list[City]) -> None:
    for city in data:
        kitchen.cities.append(city)
    await session.commit()

@connection
async def get_kitchen(session, tg_id: int) -> Kitchen|None:
    kitchen = await session.scalar(select(Kitchen).where(Kitchen.user_id==tg_id))
    if kitchen:
        return kitchen
    return None


@connection
async def test(session) ->None:
    await create_kitchen(data={'tg_id':1, 'title': "first", 'description':"text", 'number':"12345"})
