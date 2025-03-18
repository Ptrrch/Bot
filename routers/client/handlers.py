from aiogram import Router, types, F
from aiogram.enums import ParseMode

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from database.crud.clients_crud import create_client

from .states import Client

router = Router(name=__name__)



async def send_client_result(message: types.Message, data: dict):
    text = markdown.text(
        "Так выглядит твой профиль:",
        "",
        markdown.text("Имя: ", markdown.hbold(data['name'])),
        markdown.text("Фамилия: ", markdown.hbold(data['lastname'])),
        markdown.text("Адрес: ", markdown.hbold(data['address'])),
        markdown.text("Номер телефона: ", markdown.hbold(data['number'])),
        sep="\n"
    )

    await message.answer(text=text, parse_mode=ParseMode.HTML)
    await create_client(data, message.from_user.id)



@router.message(Command("client", prefix="!/"))
async def handle_start_client(message: types.Message, state: FSMContext):
    await state.set_state(Client.name)
    await message.answer(text="Добро пожаловать\nКак тебя зовут?")


@router.message(Client.name, F.text)
async def handle_client_user_full_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Client.lastname)
    await message.answer(
        f"Привет, {markdown.hbold(message.text)}, укажи пожалуйста свою фамилию",
        parse_mode=ParseMode.HTML,
    )


@router.message(Client.name)
async def handle_client_user_full_name_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )

@router.message(Client.lastname, F.text)
async def handle_client_lastname_message(message: types.Message, state: FSMContext):
    await state.update_data(lastname=message.text)
    await state.set_state(Client.address)
    await message.answer(
        "Приятно познакомится, теперь укажи свой адрес"
    )

@router.message(Client.lastname)
async def handle_client_user_lastname_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )

@router.message(Client.address, F.text)
async def handle_client_address_message(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(Client.number)
    await message.answer(
        f"Замечательно, осталось только указать номер телефона\nвведи его в формате {markdown.underline("+79991234455")}"
    )


@router.message(Client.address)
async def handle_client_user_address_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )


@router.message(Client.number, F.text)
async def handle_client_number_message(message: types.Message, state: FSMContext):
    data = await state.update_data(number=message.text)
    await state.clear()
    await send_client_result(message, data)

@router.message(Client.number)
async def handle_client_user_number_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )

