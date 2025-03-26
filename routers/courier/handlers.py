from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from Keyboards.Courier_kb import create_city_for_courier_keyboard
from Keyboards.Kitchen_kb import create_city_for_kitchen_keyboard
from database.crud.cities_crud import get_city, get_one_city
from database.crud.clients_crud import create_client
from database.crud.couriers_crud import create_courier
from database.crud.kitchens_crud import create_kitchen

from .states import Courier

router = Router(name=__name__)



async def send_courier_result(message: types.Message, data: dict):
    city = await get_one_city(data['city_id'])
    text = markdown.text(
        "Так выглядит ваш профиль:",
        "",
        markdown.text("Имя: ", markdown.hbold(data['name'])),
        markdown.text("Фамилия: ", markdown.hbold(data['lastname'])),
        markdown.text("Город: ", markdown.hbold(city.title)),
        markdown.text("Номер телефона: ", markdown.hbold(data['number'])),
        sep="\n"
    )

    await message.answer(text=text, parse_mode=ParseMode.HTML)
    await create_courier(data, message.from_user.id)





@router.message(Command("courier", prefix="!/"))
async def handle_start_kitchen(message: types.Message, state: FSMContext):
    await state.set_state(Courier.name)
    await message.answer(text="Укажите ваше имя")


@router.message(Command("cancel"))  # Сработает при команде /cancel
@router.message(F.text.casefold() == "cancel") # И если в сообщение есть "cancel"
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()  # Получаем текущий state
    if current_state is None:  # Если его нет, то ничего не возвращаем
        return
    '''А вот иначе, завершаем state и прописываем в лог'''
    await state.clear()
    await message.answer(f"Вы отменили действие: {current_state}")


@router.message(Courier.name, F.text)
async def handle_kitchen_title(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Courier.lastname)
    await message.answer("Укажите вашу фамилию")


@router.message(Courier.name)
async def handle_kitchen_title_invalid_content_type(message: types.Message):
    await message.answer(
        "Простите, я не понимаю, напишите текстом, пожалуйста"
    )


@router.message(Courier.lastname, F.text)
async def handle_kitchen_description(message: types.Message, state: FSMContext):
    await state.update_data(lastname=message.text)
    await state.set_state(Courier.city_id)
    city = await get_city()
    await message.answer("Выберите город", reply_markup=create_city_for_courier_keyboard(city))
    

@router.message(Courier.lastname)
async def handle_kitchen_description_invalid_content_type(message: types.Message):
    await message.answer(
        "Простите, я не понимаю, напишите текстом, пожалуйста"
    )


@router.callback_query(Courier.city_id, F.data.startswith('add_city_for_courier_'))
async def handle_kitchen_city_id(call: CallbackQuery, state: FSMContext):
    await call.answer()
    city_id = int(call.data.replace('add_city_for_courier_', ''))
    await state.update_data(city_id = city_id)
    await state.set_state(Courier.number)
    await call.message.answer(
        "Укажите ваш номер"
    )

@router.message(Courier.city_id)
async def handle_kitchen_city_id_invalid_content_type(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Выберите город из списка")



@router.message(Courier.number, F.text)
async def handle_kitchen_number(message: types.Message, state: FSMContext):
    data = await state.update_data(number=message.text)
    await state.clear()
    await send_courier_result(message, data)
    
    

@router.message(Courier.number)
async def handle_kitchen_number_invalid_content_type(message: types.Message):
    await message.answer(
        "Простите, я не понимаю, напишите текстом, пожалуйста"
    )

