from aiogram import Router, types
from aiogram.filters import CommandStart, Command

from Keyboards.Base_kb import main_kb, client_profile_kb, agree_with_form_kb, kitchen_kb, courier_kb, admin_kb
from database.crud.admins_crud import get_admin, delete_admin
from database.crud.clients_crud import get_client, create_client
from database.crud.user_crud import create_user, get_user_id, get_user_form
from database.models import UserForm
from filters.getRole import RoleFilter
from filters.isKitchen import KitchenFilter

router = Router(name=__name__)
router.message.filter(RoleFilter())

@router.message(CommandStart(), RoleFilter())
async def start_message(message: types.Message, role: dict):
    if role == "Kitchen":
        await message.answer("Кухня", reply_markup=kitchen_kb())
    elif role == "Admin":
        await message.answer("Админ", reply_markup=admin_kb())
    elif role == "Courier":
        await message.answer("Курьер", reply_markup=courier_kb())
    else:
        await create_user(message.from_user.id)
        if await get_user_form(message.from_user.id) == UserForm.disagree:
            await message.answer(text="Приветствуем вас", reply_markup=main_kb())
            await message.answer("Согласие на обработку данных", reply_markup=agree_with_form_kb(message.from_user.id))

        else:
            await message.answer("Приветствуем вас", reply_markup=main_kb())

@router.message(Command("id", prefix="!/"))
async def start_message(message: types.Message):
    idx = await get_user_id(message.from_user.id)
    await message.answer(text=f"Ваш id: {idx}", reply_markup=main_kb())



@router.message(Command("help", prefix="!/"))
async def help_message(message: types.Message):
    await message.answer(text="Sorry,i want to help you, but i don't")



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


