import asyncio

from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InputMediaPhoto

from Keyboards.City_kb import create_city_keyboard, city_change_keyboard
from Keyboards.Client_kb import create_kitchen_for_client_keyboard, create_product_from_kitchen_keyboard, \
    interface_from_item
from database.crud.cities_crud import get_city, get_one_city, delete_city
from database.crud.kitchens_crud import get_kitchen, get_kitchens
from database.crud.product_crud import get_products, get_one_product

router = Router(name=__name__)


@router.message(F.text == '📚 Каталог заведений')
async def get_kitchen_table(message: types.Message) ->None:
    data = await get_kitchens()
    await message.answer(text="Список Заведений: ", reply_markup=create_kitchen_for_client_keyboard(data))


@router.callback_query(F.data.startswith('get_kitchen_list'))
async def back_to_kitchen_list(call: CallbackQuery):
    data = await get_kitchens()
    await call.message.edit_text(text="Список Заведений: ", reply_markup=create_kitchen_for_client_keyboard(data))


@router.callback_query(F.data.startswith('get_kitchen_for_client_item_'))
async def get_products_from_kitchen(call: CallbackQuery):
    await call.answer()
    kitchen_id = int(call.data.replace('get_kitchen_for_client_item_', ''))
    kitchen = await get_kitchen(kitchen_id)
    data = await get_products({'owned_id': kitchen_id})

    # Проверяем, есть ли текст в сообщении
    if call.message.text:
        await call.message.edit_text(f"Вот список блюд из {kitchen.title}",
                                     reply_markup=create_product_from_kitchen_keyboard(data))
    else:
        # Если текста нет, отправляем новое сообщение
        await call.message.answer(f"Вот список блюд из {kitchen.title}",
                                  reply_markup=create_product_from_kitchen_keyboard(data))


@router.callback_query(F.data.startswith('get_item_from_kitchen_'))
async def get_item_in_product(call: CallbackQuery):
    await call.answer()
    product_id = int(call.data.replace('get_item_from_kitchen_', ''))

    try:
        product = await get_one_product({'id': product_id})
        kitchen_id = product.owned_id

        # Проверяем, есть ли текст в сообщении
        if call.message and call.message.text:
            media = InputMediaPhoto(media=str(product.img),caption=f"Название: {product.title}\nОписание: {product.description}\nСтоимость: {product.price} - руб")
            await call.message.edit_media(media=media, reply_markup=interface_from_item(int(kitchen_id)))
    except Exception as e:
        await call.message.answer("Произошла ошибка при получении информации о продукте.")
        print(f"Ошибка: {e}")


@router.callback_query(F.data.startswith('delete_city_'))
async def delete_city_from_city_table(call: CallbackQuery):
    await call.answer()
    city_id = int(call.data.replace('delete_city_', ''))
    data = {}
    data['id'] = int(city_id)
    await delete_city(data)
    await call.message.answer(text=f"Город под номером {city_id} успешно удален", reply_markup=None)