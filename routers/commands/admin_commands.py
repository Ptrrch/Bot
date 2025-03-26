from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command

from Keyboards.Admin_kb import create_admin_keyboard


router = Router(name=__name__)


@router.message(F.text == "admin")
async def hello_admin(message: types.Message):
    await message.answer("Привет админ", reply_markup=create_admin_keyboard())