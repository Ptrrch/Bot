from aiogram import types
from aiogram.filters import Filter

from database.crud.couriers_crud import get_couriers
from database.crud.kitchens_crud import get_kitchens



class CourierFilter(Filter):
    async def __call__(self, message: types.Message):
        couriers = await get_couriers()
        couriers_id = [item.user_id for item in couriers]
        return message.from_user.id in couriers_id