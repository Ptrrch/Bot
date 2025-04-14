from aiogram import types
from aiogram.filters import Filter

from database.config import settings
from database.crud.admins_crud import get_admins
from database.crud.clients_crud import get_clients
from database.crud.couriers_crud import get_couriers




class AdminsFilter(Filter):
    async def __call__(self, message: types.Message):
        admins = settings.admins
        admins_from_database = await get_admins()
        admins_list = [item.user_id for item in admins_from_database]
        return message.from_user.id in admins or message.from_user.id in admins_list