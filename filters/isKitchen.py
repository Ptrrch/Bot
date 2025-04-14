from aiogram import types
from aiogram.filters import Filter

from database.crud.kitchens_crud import get_kitchens



class KitchenFilter(Filter):
    async def __call__(self, message: types.Message):
        kitchens = await get_kitchens()
        kitchens_id = [item.user_id for item in kitchens]
        return message.from_user.id in kitchens_id
