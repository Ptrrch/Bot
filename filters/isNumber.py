from aiogram import types
from aiogram.filters import Filter

class IsNumberFilter(Filter):
     async def __call__(self, message: types.Message):
        return message.text.isdigit()