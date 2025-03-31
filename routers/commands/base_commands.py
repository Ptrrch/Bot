from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from Keyboards.Base_kb import main_kb
from database.crud.admins_crud import get_admin, delete_admin
from database.crud.clients_crud import get_client
from database.crud.user_crud import create_user, get_user_id

router = Router(name=__name__)


@router.message(CommandStart())
async def start_message(message: types.Message):
    await message.answer(text="Holla, i'm demo-Bot", reply_markup=main_kb())
    await create_user(message.from_user.id)

@router.message(Command("id", prefix="!/"))
async def start_message(message: types.Message):
    idx = await get_user_id(message.from_user.id)
    await message.answer(text=f"Ваш id: {idx}", reply_markup=main_kb())



@router.message(Command("help", prefix="!/"))
async def help_message(message: types.Message):
    await message.answer(text="Sorry,i want to help you, but i don't")


@router.message(Command("get_client", prefix="!/"))
async def get_message_user(message: types.Message):
    data = await get_client(message.from_user.id)
    if data:
        await message.answer(
            f"ID: {data.id}\n"
            f"Telegram ID: {data.user_id}\n"
            f"Имя: {data.name}\n"
            f"Фамилия: {data.lastname}\n"
            f"Адрес: {data.address}\n"
            f"Состояние: {data.state}\n"
            f"Номер: {data.number}"
        )
    else:
        await message.answer("Клиент не найден.")

@router.message(Command("get_admin", prefix="!/"))
async def get_admin_profile(message: types.Message):
    data = await get_admin(message.from_user.id)
    if data:
        await message.answer(
            f"ID: {data.id}\n"
            f"Telegram ID: {data.user_id}\n"
            f"Имя: {data.name}\n"
            f"Фамилия: {data.lastname}\n"
            f"Номер: {data.number}"
        )
    else:
        await message.answer("Админ не найден.")

@router.message(Command("delete_admin", prefix="!/"))
async def get_admin_profile(message: types.Message):
    data = await get_admin(message.from_user.id)
    if data:
        await delete_admin(message.from_user.id)
        await message.answer(f"Админ номер {message.from_user.id} успешно удален")
    else:
        await message.answer("Админ не найден.")


@router.message(Command('menu', prefix="!/"))
async def list_of_establishments(message: types.Message):
    ...

