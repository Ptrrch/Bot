from aiogram import types
from aiogram.filters import Filter

from database.crud.clients_crud import get_client
from database.crud.user_crud import get_users_agree


class CustomFilter(Filter):
    async def __call__(self, message: types.Message):
        users_id = await get_users_agree()
        if message.from_user.id in users_id:
            return {'agreement': True}
        return {'agreement': False}

class CustomClientFilter(Filter):
    async def __call__(self, message: types.Message):
        user_id = await get_client(message.from_user.id)
        if user_id:
            return {'client': True}
        return {'client': False}