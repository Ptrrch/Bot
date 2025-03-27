import asyncio

from Keyboards.Product_kb import create_product_keyboard, product_change_keyboard
from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from Keyboards.City_kb import  city_change_keyboard

from database.crud.product_crud import delete_product, get_one_product, get_products
from routers.city.states import City

router = Router(name=__name__)

@router.callback_query(F.data.startswith('back_home'))
@router.message(Command("get_product", prefix="!/"))
async def get_product_table(message: types.Message) ->None:
    data = await get_products({'owned_id': 1})
    await message.answer(text="Список Позиций:", reply_markup=create_product_keyboard(data))


@router.callback_query(F.data.startswith('refresh_product'))
async def refresh_product_tablet(call: CallbackQuery):
    await call.answer()
    data = await get_products({'owned_id': 1})
    await call.message.answer("Вот новая клавиатура", reply_markup=create_product_keyboard(data))


@router.callback_query(F.data.startswith('get_product_item_'))
async def get_item_from_product_table(call: CallbackQuery):
    await call.answer()
    product_id = int(call.data.replace('get_product_item_', ''))
    data = await get_one_product({'id': product_id})
    img = data.img
    text = f"Наименование: {data.title}\nОписание: {data.description}\nСтоимость: {data.price}"
    await call.message.answer_photo(photo = img, caption = text, reply_markup=product_change_keyboard(product_id))





@router.callback_query(F.data.startswith('delete_product_'))
async def delete_product_from_product_table(call: CallbackQuery):
    await call.answer()
    product_id = int(call.data.replace('delete_product_', ''))
    data = {}
    data['id'] = int(product_id)
    await delete_product(data)
    await call.message.answer(text=f"Позиция под номером {product_id} успешно удалена", reply_markup=None)