from aiogram import Router, types, F
from aiogram.enums import ParseMode

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import ReplyKeyboardRemove
from aiogram.utils import markdown

from database.crud.admins_crud import create_admin, get_admin, update_admin

from .states import Admin, AdminUpdate

router = Router(name=__name__)


def auxiliary_kb(text: str):
    print(text)
    new_kb = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text = f"{text}")],
            ],
            resize_keyboard=True
        )
    return new_kb

async def send_admins_result(message: types.Message, data: dict):
    text = markdown.text(
        "Так выглядит твой профиль:",
        "",
        markdown.text("Имя: ", markdown.hbold(data['name'])),
        markdown.text("Фамилия: ", markdown.hbold(data['lastname'])),
        markdown.text("Номер телефона: ", markdown.hbold(data['number'])),
        sep="\n"
    )

    await message.answer(text=text, parse_mode=ParseMode.HTML)
    await create_admin(data, message.from_user.id)


async def send_admins_update_result(message: types.Message, data: dict):
    text = markdown.text(
        "Так теперь выглядит твой профиль: ",
        "",
        markdown.text("Имя: ", markdown.hbold(data['name'])),
        markdown.text("Фамилия: ", markdown.hbold(data['lastname'])),
        markdown.text("Номер телефона: ", markdown.hbold(data['number'])),
        sep="\n"
    )

    await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=ReplyKeyboardRemove())
    await update_admin(data, message.from_user.id)


@router.message(Command("create_admin", prefix="!/"))
async def handle_start_client(message: types.Message, state: FSMContext):
    await state.set_state(Admin.name)
    await message.answer(text="Укажи свое имя")


@router.message(Command("cancel"))  # Сработает при команде /cancel
@router.message(F.text.casefold() == "cancel") # И если в сообщение есть "cancel"
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()  # Получаем текущий state
    if current_state is None:  # Если его нет, то ничего не возвращаем
        return
    '''А вот иначе, завершаем state и прописываем в лог'''
    await state.clear()
    await message.answer(f"Вы отменили действие: {current_state}")


@router.message(Admin.name, F.text)
async def handle_client_user_full_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Admin.lastname)
    await message.answer("Укажи свою фамилию")


@router.message(Admin.name)
async def handle_client_user_full_name_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )

@router.message(Admin.lastname, F.text)
async def handle_client_lastname_message(message: types.Message, state: FSMContext):
    await state.update_data(lastname=message.text)
    await state.set_state(Admin.number)
    await message.answer(
        f"Понял, теперь укажи свой номер телефона\nвведи его в формате {markdown.underline("+79991234455")}"
    )

@router.message(Admin.lastname)
async def handle_client_user_lastname_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )

@router.message(Admin.number, F.text)
async def handle_client_address_message(message: types.Message, state: FSMContext):
    data = await state.update_data(number=message.text)
    await state.clear()
    await send_admins_result(message, data)


@router.message(Admin.number)
async def handle_client_user_address_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )



@router.message(Command("update_admin", prefix="!/"))
async def handle_start_admin(message: types.Message, state: FSMContext):
    data = await get_admin(message.from_user.id)
    await state.set_state(AdminUpdate.name)
    await message.answer("Укажи новое имя",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer("Если хотите оставить прошлое, нажмите на кнопку: ",
                         reply_markup=auxiliary_kb(data.name))


@router.message(AdminUpdate.name, F.text)
async def handle_client_user_full_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AdminUpdate.lastname)
    data = await get_admin(message.from_user.id)
    await message.answer(text="Если хотите оставить прошлую, нажмите на кнопку: ",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "Укажи новую фамилию",
        reply_markup=auxiliary_kb(data.lastname))


@router.message(Admin.name)
async def handle_admin_invalid_input(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )


@router.message(AdminUpdate.lastname, F.text)
async def handle_client_lastname_message(message: types.Message, state: FSMContext):
    await state.update_data(lastname=message.text)
    await state.set_state(AdminUpdate.number)
    data = await get_admin(message.from_user.id)
    await message.answer(text="Если хотите оставить прошлый, нажмите на кнопку: ",
                         reply_markup=ReplyKeyboardRemove())
    await message.answer(
        "Теперь укажи новый номер телефона",
        reply_markup=auxiliary_kb(data.number)
    )

@router.message(AdminUpdate.lastname)
async def handle_admin_invalid_input(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )

@router.message(AdminUpdate.number, F.text)
async def handle_client_address_message(message: types.Message, state: FSMContext):
    data = await state.update_data(number=message.text)
    await state.clear()
    await send_admins_update_result(message, data)


@router.message(AdminUpdate.number)
async def handle_admin_invalid_input(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )



