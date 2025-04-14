import asyncio

from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from Keyboards.City_kb import city_change_keyboard
from database.crud.cities_crud import get_city, get_one_city, delete_city


router = Router(name=__name__)

