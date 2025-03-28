from aiogram import Router, F
from aiogram.client.default import Default
from aiogram.enums import ParseMode
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from Keyboards.Product_kb import ProductCbData, ProductActions, product_change_keyboard, create_product_keyboard
from database.crud.kitchens_crud import get_kitchen
from database.crud.product_crud import get_one_product, get_products, delete_product

router = Router(name=__name__)



@router.callback_query(ProductCbData.filter(F.action == ProductActions.details))
async def show_product_details(call: CallbackQuery, callback_data: ProductCbData):
    await call.answer()
    product = await get_one_product({'id': callback_data.id})


    text = f"{product.title}\n{product.description}\nЦена: {product.price}.р"

    await call.message.answer_photo(
        photo=product.img,
        caption=text,
        reply_markup=product_change_keyboard(callback_data.id)
    )


@router.callback_query(ProductCbData.filter(F.action == ProductActions.delete))
async def show_product_details(call: CallbackQuery, callback_data: ProductCbData):
    product = await get_one_product({'id': callback_data.id})
    await delete_product({'id': callback_data.id})
    products = await get_products({'owned_id': product.owned_id})
    kitchen = await get_kitchen(product.owned_id)
    keyboard = create_product_keyboard(kitchen.id, kitchen.title, products)


    if call.message.text:
        await call.message.edit_text(text=kitchen.title, reply_markup=keyboard)
    else:

        await call.message.answer(text=kitchen.title, reply_markup=keyboard)


@router.callback_query(ProductCbData.filter(F.action == ProductActions.back))
async def show_product_details(call: CallbackQuery):
    await call.message.delete()