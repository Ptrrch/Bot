from aiogram import types
from aiogram.filters import Filter

from database.config import settings
from database.crud.admins_crud import get_admin, get_admins
from database.crud.couriers_crud import get_couriers
from database.crud.kitchens_crud import get_kitchens



class RoleFilter(Filter):
    async def __call__(self, message: types.Message):
        kitchens = await get_kitchens()
        kitchens_id = [item.user_id for item in kitchens]
        couriers = await get_couriers()
        couriers_id = [item.user_id for item in couriers]
        admins = await get_admins()
        admins_list = settings.admins
        admins_id = [item.user_id for item in admins]
        if message.from_user.id in kitchens_id:
            return {'role': "Kitchen"}
        elif message.from_user.id in couriers_id:
            return {'role': "Courier"}
        elif message.from_user.id in admins_id or message.from_user.id in admins_list:
            return {'role': "Admin"}
        else:
            return {'role': "Client"}