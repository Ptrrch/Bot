from sqlalchemy import select
from sqlalchemy.orm import selectinload

from database.crud.cities_crud import create_city
from database.engine import connection
from database.models import Courier, City


@connection
async def create_courier(session, data: dict, tg_id: int) -> None:
    courier = await session.scalar(select(Courier).where(Courier.user_id == tg_id))
    if not courier:
        new_courier = Courier(
            user_id = tg_id,
            name = data['name'],
            lastname = data['lastname'],
            number = data['number'],
            city_id = data['city_id']
        )
        session.add(new_courier)
        await session.commit()
    else:
        print("Такой курьер уже есть")




@connection
async def append_courier_to_city(session, tg_id: int, city_id: int) -> None:
    print(f"Запрашиваем город с id: {city_id}")

    city = await session.scalar(
        select(City)
        .options(selectinload(City.couriers))
        .where(City.id == city_id)
    )

    if city is None:
        print(f"Город с id {city_id} не найден.")
        return

    courier = await session.scalar(select(Courier).where(Courier.id == tg_id))

    if courier is None:
        print("Не удалось найти курьера")
        return

    city.couriers.append(courier)
    await session.commit()


@connection
async def get_couriers(session) ->list[Courier]|None:
    couriers = await session.scalars(select(Courier))
    if couriers:
        return couriers
