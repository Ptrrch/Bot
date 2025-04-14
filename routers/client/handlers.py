from aiogram import Router, types, F
from aiogram.enums import ParseMode

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from Keyboards.Admin_kb import AdminClientCbData, AdminClientActions
from Keyboards.Base_kb import ClientProfileCb, ClientProfileActions, contact_kb, main_kb
from Keyboards.Client_kb import ClientCbData, ClientActions
from Keyboards.Courier_kb import create_city_for_courier_keyboard, create_city_for_client_keyboard
from Keyboards.Product_kb import ProductCbData, ProductActions
from database.crud.cities_crud import get_city, get_one_city
from database.crud.clients_crud import create_client, update_client

from .states import Client, UpdateClient

router = Router(name=__name__)



async def send_client_result(message: types.Message, data: dict):
    city = await get_one_city(data['city_id'])
    text = markdown.text(
        "Так выглядит твой профиль:",
        "",
        markdown.text("Имя: ", markdown.hbold(data['name'])),
        markdown.text("Фамилия: ", markdown.hbold(data['lastname'])),
        markdown.text("Отчество: ", markdown.hbold(data['patronymic'])),
        markdown.text("Номер телефона: ", markdown.hbold(data['number'])),
        markdown.text("Город: ", markdown.hbold(city.title)),
        sep="\n"
    )

    await message.answer(text=text, parse_mode=ParseMode.HTML, reply_markup=main_kb())
    await create_client(data)



async def send_client_update_result(data, message: types.Message):
    text = markdown.text(
        "Так теперь выглядит твой профиль:",
        "",
        markdown.text("Имя: ", markdown.hbold(data['name'])),
        markdown.text("Фамилия: ", markdown.hbold(data['lastname'])),
        markdown.text("Номер телефона: ", markdown.hbold(data['number'])),
        sep="\n"
    )

    await message.answer(text=text, parse_mode=ParseMode.HTML)
    await update_client(data)



@router.callback_query(AdminClientCbData.filter(F.action == AdminClientActions.create))
async def handle_start_admin_client(call: CallbackQuery, callback_data:AdminClientCbData, state: FSMContext):
    await state.set_state(Client.name)
    await call.message.answer(text="Укажите имя пользователя")


@router.callback_query(ClientProfileCb.filter(F.action == ClientProfileActions.create))
async def handle_start_admin_client(call: CallbackQuery, callback_data:ClientProfileCb, state: FSMContext):
    await state.set_state(Client.id)
    await state.update_data(id = callback_data.id)
    await state.set_state(Client.name)
    await call.message.answer(text="Укажите имя пользователя")

@router.message(Command("cancel"))  # Сработает при команде /cancel
@router.message(F.text.casefold() == "cancel") # И если в сообщение есть "cancel"
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()  # Получаем текущий state
    if current_state is None:  # Если его нет, то ничего не возвращаем
        return
    '''А вот иначе, завершаем state и прописываем в лог'''
    await state.clear()
    await message.answer(f"Вы отменили действие: {current_state}")


@router.message(Client.name, F.text)
async def handle_client_user_full_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Client.lastname)
    await message.answer(
        f"Привет, {markdown.hbold(message.text)}, укажите, пожалуйста, свою фамилию",
        parse_mode=ParseMode.HTML,
    )


@router.message(Client.name)
async def handle_client_user_full_name_invalid_content_type(message: types.Message):
    await message.answer(
        "Простите, я не понимаю, напишите текстом, пожалуйста"
    )



@router.message(Client.lastname, F.text)
async def handle_client_lastname_message(message: types.Message, state: FSMContext):
    await state.update_data(lastname=message.text)
    await state.set_state(Client.patronymic)
    await message.answer("Пожалуйста, укажите ваше отчество")


@router.message(Client.lastname)
async def handle_client_user_lastname_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напишите текстом, пожалуйста"
    )

@router.message(Client.patronymic, F.text)
async def handle_client_lastname_message(message: types.Message, state: FSMContext):
    await state.update_data(patronymic=message.text)
    await state.set_state(Client.city_id)
    city = await get_city()
    await message.answer("Выберите город", reply_markup=create_city_for_client_keyboard(city))

@router.message(Client.patronymic)
async def handle_client_user_lastname_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напишите текстом, пожалуйста"
    )

@router.callback_query(Client.city_id, F.data.startswith('add_city_for_client_'))
async def handle_client_city_id(call: CallbackQuery, state: FSMContext):
    await call.answer()
    city_id = int(call.data.replace('add_city_for_client_', ''))
    await state.update_data(city_id = city_id)
    await state.set_state(Client.number)
    await call.message.answer("Пожалуйста, отправьте ваш номер телефона", reply_markup=contact_kb())


@router.message(Client.number, F.contact)
async def handle_client_number_message(message: types.Message, state: FSMContext):
    number = message.contact.phone_number
    data = await state.update_data(number=number)
    await state.clear()
    await send_client_result(message, data)

@router.message(Client.number)
async def handle_client_user_number_invalid_content_type(message: types.Message):
    await message.answer(
        "Нажмите на кнопку, пожалуйста", reply_markup=contact_kb()
    )


@router.callback_query(
    ClientCbData.filter(F.action == ClientActions.update)
)
async def update_client_info(call: CallbackQuery, callback_data:ClientCbData, state: FSMContext):
    await call.answer()
    await state.set_state(UpdateClient.user_id)
    tg_id = callback_data.id
    await state.update_data(user_id = tg_id)
    await state.set_state(UpdateClient.name)
    await call.message.answer("Введите новое имя")


@router.message(UpdateClient.name, F.text)
async def handle_client_user_full_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(UpdateClient.lastname)
    await message.answer(
        f"Введите новую фамилию",
        parse_mode=ParseMode.HTML,
    )


@router.message(UpdateClient.name)
async def handle_client_user_full_name_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )


@router.message(UpdateClient.lastname, F.text)
async def handle_client_lastname_message(message: types.Message, state: FSMContext):
    await state.update_data(lastname=message.text)
    await state.set_state(UpdateClient.number)
    await message.answer(
        "Теперь укажите новый номер"
    )


@router.message(UpdateClient.lastname)
async def handle_client_user_lastname_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )

@router.message(UpdateClient.number, F.text)
async def handle_client_number_message(message: types.Message, state: FSMContext):
    data = await state.update_data(number=message.text)
    await state.clear()
    await send_client_update_result(data, message)


@router.message(UpdateClient.number)
async def handle_client_user_number_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )

