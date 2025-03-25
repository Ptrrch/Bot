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
async def create_city_message(message: types.Message, state: FSMContext):
    await state.set_state(City.title)
    await message.answer("Введите название города")


@router.message(City.title, F.text)
async def create_city_title(message:types.Message, state: FSMContext):
    data = await state.update_data(title = message.text)
    await message.answer(f"{data['title']} успешно добавлен")
    await send_city_result(data)
    await state.clear()

@router.callback_query(F.data.startswith('change_city_'))
async def update_city(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(ChangeCity.id)
    city_id = int(call.data.replace('change_city_', ''))
    await state.update_data(id = city_id)
    await state.set_state(ChangeCity.title)


@router.message(ChangeCity.title, F.text)
async def create_city_title(message:types.Message, state: FSMContext):
    data = await state.update_data(title = message.text)
    await state.clear()
    await update_city(data)
    await message.answer(f"{data['title']} успешно изменен")

