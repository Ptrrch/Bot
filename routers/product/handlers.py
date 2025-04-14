from aiogram import Router, types, F
from aiogram.enums import ParseMode
from aiogram.fsm.state import default_state
from aiogram.types import CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.utils import markdown

from Keyboards.Kitchen_kb import KitchenMenuCb, KitchenMenuActions, KitchenMenuItemCb, KitchenMenuItemActions
from Keyboards.Product_kb import create_kitchen_for_product_keyboard, ProductCbData, ProductActions
from database.crud.kitchens_crud import get_kitchens
from database.crud.product_crud import create_product, update_product

from .states import ChangeProduct, Product

router = Router(name=__name__)



async def send_product_result(message: types.Message, data: dict):
    text = markdown.text(
        "Так выглядит товар:",
        "",
        markdown.text("Наименование: ", markdown.hbold(data['title'])),
        markdown.text("Описание: ", markdown.hbold(data['description'])),
        markdown.text("Стоимость: ", markdown.hbold(data['price'])),
        markdown.text("Номер владельца: ", markdown.hbold(data['owned_id'])),
        sep="\n"
    )

    await message.answer_photo(photo=data['img'], caption=text, parse_mode=ParseMode.HTML)
    await create_product(data)

@router.callback_query(KitchenMenuCb.filter(F.action == KitchenMenuActions.append))
async def handle_start_client(call: CallbackQuery, callback_data:KitchenMenuCb, state: FSMContext):
    await call.answer()
    await state.set_state(Product.owned_id)
    await state.update_data(owned_id=callback_data.kitchen_id)
    await state.set_state(Product.title)
    await call.message.answer(text="Укажите наименование позиции")


@router.callback_query(ProductCbData.filter(F.action == ProductActions.create))
async def handle_start_client(call: CallbackQuery, callback_data:ProductCbData, state: FSMContext):
    await call.answer()
    await state.set_state(Product.owned_id)
    await state.update_data(owned_id=callback_data.id)
    await state.set_state(Product.title)
    await call.message.answer(text="Укажите наименование позиции")


@router.message(Command("cancel"))  # Сработает при команде /cancel
@router.message(F.text.casefold() == "cancel") # И если в сообщение есть "cancel"
async def cancel_handler(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()  # Получаем текущий state
    if current_state is None:  # Если его нет, то ничего не возвращаем
        return
    '''А вот иначе, завершаем state и прописываем в лог'''
    await state.clear()
    await message.answer(f"Вы отменили действие: {current_state}")



@router.message(Product.title, F.text)
async def handle_client_user_full_name(message: types.Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(Product.description)
    await message.answer(
       text = "Укажите описание товара"
    )




@router.message(Product.description, F.text)
async def handle_client_lastname_message(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Product.price)
    await message.answer(
        "Укажите стоимость товара"
    )

@router.message(Product.description)
async def handle_client_user_full_name_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )

@router.message(Product.price, F.text)
async def handle_client_address_message(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(Product.img)
    await message.answer(
        "Отправьте фотографию товара"
    )

@router.message(Product.price)
async def handle_client_user_lastname_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )


@router.message(Product.img, F.photo)
async def handle_client_number_message(message: types.Message, state: FSMContext):
    data = await state.update_data(img=message.photo[-1].file_id)
    await state.clear()
    await send_product_result(message, data)

@router.message(Product.img)
async def handle_client_user_number_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, отправь фотографию, пожалуйста"
    )


@router.callback_query(KitchenMenuItemCb.filter(F.action == KitchenMenuItemActions.change))
async def change_product(call: CallbackQuery, callback_data: KitchenMenuItemCb, state: FSMContext):
    await call.answer()
    await state.set_state(ChangeProduct.id)

    await state.update_data(id=callback_data.product_id)

    await state.set_state(ChangeProduct.title)
    await call.message.answer("Введите новое название")


@router.callback_query(ProductCbData.filter(F.action == ProductActions.update))
async def change_product(call: CallbackQuery, callback_data:ProductCbData, state: FSMContext):
    await call.answer()
    await state.set_state(ChangeProduct.id)

    await state.update_data(id=callback_data.id)
    
    await state.set_state(ChangeProduct.title)
    await call.message.answer("Введите новое название")


@router.message(ChangeProduct.title, F.text)
async def change_product_title(message:types.Message, state: FSMContext):
    await state.update_data(title = message.text)
    await state.set_state(ChangeProduct.description)
    await message.answer("Введите новое описание")


@router.message(ChangeProduct.title)
async def product_title_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )


@router.message(ChangeProduct.description, F.text)
async def change_product_description(message: types.Message, state: FSMContext):
    await state.update_data(description = message.text)
    await state.set_state(ChangeProduct.price)
    await message.answer("Введите новую цену")

@router.message(ChangeProduct.description)
async def product_description_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )

@router.message(ChangeProduct.price, F.text)
async def change_product_price(message: types.Message, state: FSMContext):
    await state.update_data(price = message.text)
    await state.set_state(ChangeProduct.img)
    await message.answer("Отправьте новую фотографию")



@router.message(ChangeProduct.price)
async def handle_client_user_full_name_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, напиши текстом, пожалуйста"
    )


@router.message(ChangeProduct.img, F.photo)
async def change_product_img(message: types.Message, state: FSMContext):
    await state.update_data(img = message.photo[-1].file_id)
    data = await state.get_data()
    await state.clear()
    await update_product(data)

@router.message(ChangeProduct.img)
async def handle_client_user_full_name_invalid_content_type(message: types.Message):
    await message.answer(
        "Прости, я не понимаю, отправь фотографию, пожалуйста"
    )



