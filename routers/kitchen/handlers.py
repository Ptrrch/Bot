from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from Keyboards.Kitchen_kb import create_city_for_kitchen_keyboard
from database.crud.cities_crud import get_city, get_one_city
from database.crud.clients_crud import create_client
from database.crud.kitchens_crud import create_kitchen

from .states import Kitchen

router = Router(name=__name__)



async def send_kitchen_result(message: types.Message, data: dict):
    city = await get_one_city(data['city_id'])
    text = markdown.text(
        "Так выглядит профиль вашего заведения:",
        "",
        markdown.text("Название: ", markdown.hbold(data['title'])),
        markdown.text("Описание: ", markdown.hbold(data['description'])),

        markdown.text("Адрес: ", markdown.hbold(city.title),", ", markdown.hbold(data['address'])),
        markdown.text("Номер телефона: ", markdown.hbold(data['number'])),
        sep="\n"
    )

    await message.answer(text=text, parse_mode=ParseMode.HTML)
    await create_kitchen(data, message.from_user.id)



@router.message(Command("kitchen", prefix="!/"))
async def handle_start_kitchen(message: types.Message, state: FSMContext):
    await state.set_state(Kitchen.title)
    await message.answer(text="Укажите ваше название")


@router.message(Kitchen.title, F.text)
async def handle_kitchen_title(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Kitchen.description)
    await message.answer("Укажите описание вашего заведения")


@router.message(Kitchen.title)
async def handle_kitchen_title_invalid_content_type(message: types.Message):
    await message.answer(
        "Простите, я не понимаю, напишите текстом, пожалуйста"
    )


@router.message(Kitchen.description, F.text)
async def handle_kitchen_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Kitchen.city_id)
    city = await get_city()
    await message.answer("Выберите город", reply_markup=create_city_for_kitchen_keyboard(city))
    

@router.message(Kitchen.description)
async def handle_kittchen_description_invalid_content_type(message: types.Message):
    await message.answer(
        "Простите, я не понимаю, напишите текстом, пожалуйста"
    )


@router.callback_query(Kitchen.city_id, F.data.startswith('add_city_for_kitchen_'))
async def handle_kitchen_city_id(call: CallbackQuery, state: FSMContext):
    await call.answer()
    id = int(call.data.replace('add_city_for_kitchen_', ''))
    await state.update_data(city_id = id)
    await state.set_state(Kitchen.address)
    await call.message.answer(
        "Укажите адрес вашего заведения"
    )

@router.message(Kitchen.city_id)
async def handle_kitchen_city_id_invalid_content_type(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Выберите город из списка")


@router.message(Kitchen.address, F.text)
async def handle_kitchen_address(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(Kitchen.number)
    await message.answer(
        f"Укажите номер телефона вашего заедения в формате {markdown.underline("+79991234455")}"
    )


@router.message(Kitchen.address)
async def handle_kitchen_address_invalid_content_type(message: types.Message):
    await message.answer(
        "Простите, я не понимаю, напишите текстом, пожалуйста"
    )


@router.message(Kitchen.number, F.text)
async def handle_kitchen_number(message: types.Message, state: FSMContext):
    data = await state.update_data(number=message.text)
    await state.clear()
    await send_kitchen_result(message, data)
    
    

@router.message(Kitchen.number)
async def handle_kitchen_number_invalid_content_type(message: types.Message):
    await message.answer(
        "Простите, я не понимаю, напишите текстом, пожалуйста"
    )

