from aiogram import Router, types, F
from aiogram.client import bot
from aiogram.enums import ParseMode

from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import markdown
from sqlalchemy.util import await_only

from database.crud.cities_crud import create_city, update_city

from .states import City, ChangeCity

router = Router(name=__name__)


async def send_city_result(data: dict):
    await create_city(data)

@router.callback_query(F.data.startswith('create_new_city'))
@router.message(Command("create_city", prefix="!/"))
async def create_city_message(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(City.title)
    await call.message.answer("Введите название города")


@router.message(Command("cancel"))  # Сработает при команде /cancel
@router.message(F.text.casefold() == "cancel") # И если в сообщение есть "cancel"
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()  # Получаем текущий state
    if current_state is None:  # Если его нет, то ничего не возвращаем
        return
    '''А вот иначе, завершаем state и прописываем в лог'''
    await state.clear()
    await message.answer(f"Вы отменили действие: {current_state}")


@router.message(City.title, F.text)
async def create_city_title(message:types.Message, state: FSMContext):
    data = await state.update_data(title = message.text)
    await message.answer(f"{data['title']} успешно добавлен")
    await send_city_result(data)
    await state.clear()

@router.callback_query(F.data.startswith('change_city_'))
async def update_city_title(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(ChangeCity.id)
    city_id = int(call.data.replace('change_city_', ''))
    await state.update_data(id = city_id)
    await state.set_state(ChangeCity.title)
    await call.message.answer("Введите новое название города")


@router.message(ChangeCity.title, F.text)
async def create_city_title(message:types.Message, state: FSMContext):
    data = await state.update_data(title = message.text)
    await state.clear()
    await update_city(data)
    await message.answer(f"{data['title']} успешно изменен")

