import asyncio

from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from Keyboards.City_kb import create_city_keyboard, city_change_keyboard
from database.crud.admins_crud import get_admin, delete_admin
from database.crud.cities_crud import get_city, get_one_city, delete_city
from database.crud.clients_crud import get_client
from routers.city.handlers import create_city_message
from routers.city.states import City

router = Router(name=__name__)

@router.callback_query(F.data.startswith('back_home'))
@router.message(Command("get_city", prefix="!/"))
async def get_city_table(message: types.Message) ->None:
    data = await get_city()
    await message.answer(text="Список Городов:", reply_markup=create_city_keyboard(data))


@router.callback_query(F.data.startswith('refresh_city'))
async def cmd_start(call: CallbackQuery):
    await call.answer()
    data = await get_city()
    await call.message.answer("Вот новая клавиатура", reply_markup=create_city_keyboard(data))


@router.callback_query(F.data.startswith('get_city_item_'))
async def cmd_start(call: CallbackQuery):
    await call.answer()
    city_id = int(call.data.replace('get_city_item_', ''))
    data = await get_one_city(city_id)
    text = data.tittle
    await call.message.answer(text, reply_markup=city_change_keyboard(city_id))





@router.callback_query(F.data.startswith('delete_city_'))
async def cmd_start(call: CallbackQuery):
    await call.answer()
    city_id = int(call.data.replace('delete_city_', ''))
    data = {}
    data['id'] = int(city_id)
    await delete_city(data)
    await call.message.answer(text=f"Город под номером {city_id} успешно удален", reply_markup=None)