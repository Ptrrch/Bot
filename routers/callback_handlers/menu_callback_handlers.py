

from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from Keyboards.Menu_kb import MenuFirstCbData, MenyFirstActions, create_kitchen_menu, create_product_menu, \
    MenuSecondCbData, MenySecondActions, create_product_interface, MenuThirdCbData, MenyThirdActions
from database.crud.kitchens_crud import get_kitchens
from database.crud.product_crud import get_products, get_one_product

router = Router(name=__name__)


@router.message(F.text == '📚 Каталог заведений')
async def show_kitchen_list(message: types.Message) ->None:
    data = await get_kitchens()
    await message.answer(text="Список Заведений: ", parse_mode=ParseMode.MARKDOWN, reply_markup=create_kitchen_menu(data))


@router.callback_query(
    MenuSecondCbData.filter(F.action == MenySecondActions.back)
)
async def show_kitchen_list(call: MenuSecondCbData) ->None:
    data = await get_kitchens()
    await call.message.edit_text(text="Список Заведений: ", reply_markup=create_kitchen_menu(data))


@router.callback_query(
    MenuFirstCbData.filter(F.action == MenyFirstActions.back)
)
async def show_kitchen_list(call: MenuFirstCbData) ->None:
    await call.message.delete()


@router.callback_query(
    MenuFirstCbData.filter(F.action == MenyFirstActions.show)
)
async def show_kitchen_menu(call: CallbackQuery, callback_data: MenuFirstCbData):
    await call.answer()
    products = await get_products({'owned_id': callback_data.kitchen_id})
    await call.message.edit_text(text=callback_data.kitchen_title, reply_markup=create_product_menu(products, callback_data.kitchen_id))

@router.callback_query(
    MenuSecondCbData.filter(F.action == MenySecondActions.show)
)
async def show_kitchen_menu(call: CallbackQuery, callback_data: MenuSecondCbData):
    await call.answer()
    product = await get_one_product({'id': callback_data.product_id})
    text = f"{product.title}\n{product.description}\n{product.price}"
    await call.message.answer_photo(photo=product.img, caption= text, reply_markup=create_product_interface(callback_data.product_id))

@router.callback_query(
    MenuThirdCbData.filter(F.action == MenyThirdActions.back)
)
async def delete_product_answer(call: CallbackQuery):
    await call.message.delete()


@router.callback_query(
    MenuThirdCbData.filter(F.action == MenyThirdActions.append)
)
async def create_order_answer(call: CallbackQuery, callback_data: MenuThirdCbData, state: FSMContext):
    await call.message.delete()



