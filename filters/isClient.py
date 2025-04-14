from aiogram import types
from aiogram.filters import Filter

from database.crud.clients_crud import get_clients
from database.crud.couriers_crud import get_couriers
from database.crud.kitchens_crud import get_kitchens



class ClientFilter(Filter):
    async def __call__(self, message: types.Message):
        clients = await get_clients()
        clients_id = [item.user_id for item in clients]
        return message.from_user.id in clients_id