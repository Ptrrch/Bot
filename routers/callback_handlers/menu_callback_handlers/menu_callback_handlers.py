from aiogram import F, types, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto

from Keyboards.Base_kb import agree_with_form_kb, client_profile_kb, time_kb, main_kb
from Keyboards.Kitchen_kb import create_order_interface
from Keyboards.Menu_kb import MenuFirstCbData, MenyFirstActions, create_kitchen_menu, create_product_menu, \
    MenuSecondCbData, create_product_interface, MenuThirdCbData, CartCbData, \
    CartActions, MenuSecondActions, create_cart_menu, MenuThirdActions, payment_type_kb, PaymentTypeCb, \
    PaymentTypeActions
from database.crud.clients_crud import get_client
from database.crud.kitchens_crud import get_kitchens_with_city, get_kitchen
from database.crud.orders_crud import create_order, create_order_assoc, change_order_price
from database.crud.product_crud import get_products, get_one_product
from database.engine import session_maker
from database.models import PaymentType
from filters.agree_with_form import CustomFilter, CustomClientFilter
from filters.isNumber import IsNumberFilter
from routers.callback_handlers.menu_callback_handlers.states import Cart, Order

router = Router(name=__name__)
router.message.filter(CustomFilter(), CustomClientFilter())




@router.message(F.text == '📚 Каталог заведений', CustomFilter(), CustomClientFilter())
async def show_kitchen_list(message: types.Message, agreement: dict, client: dict) -> None:
    if agreement and client:
        client_item = await get_client(message.from_user.id)
        data = await get_kitchens_with_city(client_item.city_id)  # Получаем список заведений
        await message.answer(
            text="Список Заведений: ",
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=create_kitchen_menu(data)
        )
    elif not agreement:
        await message.answer(
            text="Наш бот не сможет работать, если вы не согласны на обработку данных.",
            reply_markup=agree_with_form_kb(message.from_user.id)
        )
    elif not client:
        await message.answer("Кажется у вас нет профиля, для дальнейшего сотрудничества, нужно его создать", reply_markup=client_profile_kb(message.from_user.id))





@router.callback_query(
    MenuSecondCbData.filter(F.action == MenuSecondActions.back)
)
async def show_kitchen_list(call: CallbackQuery, state: FSMContext) ->None:
    await call.answer()
    client_id = call.from_user.id
    client = await get_client(client_id)
    data = await get_kitchens_with_city(client.city_id)
    await call.message.edit_text(text="Список Заведений: ", reply_markup=create_kitchen_menu(data))
    await state.clear()


@router.callback_query(
    MenuFirstCbData.filter(F.action == MenyFirstActions.back)
)
async def show_kitchen_list(call: MenuFirstCbData) ->None:
    await call.message.delete()


@router.callback_query(
    MenuFirstCbData.filter(F.action == MenyFirstActions.show)
)
async def show_kitchen_menu(call: CallbackQuery, callback_data: MenuFirstCbData, state: FSMContext):
    await call.answer()
    products = await get_products({'owned_id': callback_data.kitchen_id})
    kitchen = await get_kitchen(callback_data.kitchen_id)
    text = f"{kitchen.title}\n\n{kitchen.description}\n{kitchen.address}\n{kitchen.number}"
    await call.message.edit_text(text=text, reply_markup=create_product_menu(products, callback_data.kitchen_id))
    await state.clear()

@router.callback_query(
    MenuSecondCbData.filter(F.action == MenuSecondActions.show)
)
async def show_kitchen_menu(call: CallbackQuery, callback_data: MenuSecondCbData, state: FSMContext):
    await call.answer()
    product = await get_one_product({'id': callback_data.product_id})
    text = f"{product.title}\n{product.description}\n{product.price}"
    await call.message.answer_photo(photo=product.img, caption= text, reply_markup=create_product_interface(callback_data.product_id))
    await state.set_state(Cart.product)

@router.callback_query(
    MenuThirdCbData.filter(F.action == MenuThirdActions.back)
)
async def delete_product_answer(call: CallbackQuery):
    await call.message.delete()


@router.callback_query(
    MenuThirdCbData.filter(F.action == MenuThirdActions.append)
)
async def append_product_in_cart(call: CallbackQuery, callback_data: MenuThirdCbData, state: FSMContext):
    product = {"id": callback_data.product_id, "count": 1}
    data = await state.get_data()
    product_items = data.get('product', [])
    if not product in product_items :
        product_items.append(product)
        await state.update_data(product=product_items)
        await call.answer("Товар добавлен в корзину")
        await call.message.delete()
    else:
        await call.answer("Товар уже в корзине")
        await call.message.delete()

@router.message(Command("show", prefix="!/"))
async def show_list_product_id(message: types.Message, state: FSMContext):
    data = await state.get_data()
    product_items = data.get('product_id', [])  # Извлекаем список
    await state.clear()
    for item in product_items:
        await message.answer(f"{item}")


@router.callback_query(
    CartCbData.filter(F.action == CartActions.back),
)
async def delete_list_kitchen_menu(call: CallbackQuery):
    await call.answer()
    await call.message.delete()


@router.callback_query(
    MenuSecondCbData.filter(F.action == MenuSecondActions.cart),
)
async def get_cart_keyboards(call: CallbackQuery, callback_data:MenuSecondActions, state: FSMContext):
    data = await state.get_data()
    product_items = data.get('product', [])
    if len(product_items) == 0:
        await call.answer("Ваша корзина пуста")
    else:
        await call.answer()
        is_first = False
        is_last = False

        product = await get_one_product({"id": product_items[0]['id']})
        count_item = len(product_items)
        if count_item == 1:
            is_last = True
            is_first = True
        if count_item > 1:
            is_first = True
        text = f"""
                {product.title}\n{product.description}\n{product.price}руб. x {product_items[0]['count']} = {product.price*product_items[0]['count']}руб.\nтовар {1} из {count_item}
                """
        keyboard = create_cart_menu(product.id, is_first, is_last, position=0, kitchen_id=callback_data.kitchen_id)
        await call.message.answer_photo(photo=product.img, caption=text, reply_markup=keyboard)


@router.callback_query(
    CartCbData.filter(F.action == CartActions.back),
)
async def delete_product_menu_keyboards(call: CallbackQuery):
    await call.message.delete()

@router.callback_query(
    CartCbData.filter(F.action == CartActions.next),
)

async def move_next_product_menu_keyboards(call: CallbackQuery, callback_data:CartCbData, state: FSMContext):
    position = callback_data.position + 1
    data = await state.get_data()
    product_items = data.get('product', [])
    product_count = len(product_items)
    is_last = False
    if position == product_count - 1:
        is_last = True
    product = await get_one_product({'id': product_items[position]['id']})
    product_id = product.id
    text = f"""
        {product.title}\n{product.description}\n{product.price}руб. x {product_items[position]['count']} = {product.price * product_items[position]['count']}руб.\nтовар {position + 1} из {product_count}
        """
    keyboard = create_cart_menu(product_id, False, is_last, position=position, kitchen_id=callback_data.kitchen_id)
    media = InputMediaPhoto(media=product.img,caption=text)
    await call.message.edit_media(media=media, reply_markup=keyboard)


@router.callback_query(
    CartCbData.filter(F.action == CartActions.last),
)
async def move_last_product_menu_keyboards(call: CallbackQuery, callback_data: CartCbData, state: FSMContext):
    position = callback_data.position - 1
    data = await state.get_data()
    product_items = data.get('product', [])
    product_count = len(product_items)
    is_first = False
    if position == 0:
        is_first = True
    product = await get_one_product({'id': product_items[position]['id']})
    product_id = product.id
    text = f"""
            {product.title}\n{product.description}\n{product.price}руб. x {product_items[position]['count']} = {product.price * product_items[position]['count']}руб.\nтовар {position + 1} из {product_count}
            """
    keyboard = create_cart_menu(product_id, is_first, False, position=position,kitchen_id=callback_data.kitchen_id)
    media = InputMediaPhoto(media=product.img,caption=text)
    await call.message.edit_media(media=media, reply_markup=keyboard)


@router.callback_query(
    CartCbData.filter(F.action == CartActions.delete),
)
async def delete_product_in_cart(call: CallbackQuery, callback_data: CartCbData, state: FSMContext):
    position = callback_data.position
    data = await state.get_data()
    product_items = data.get('product', [])
    product_items.pop(position)
    await state.update_data(product=product_items)

    count_item = len(product_items)

    if count_item == 0:
        await call.answer("Ваша корзина пуста")
        await call.message.delete()
    else:
        await call.answer()
        if position >= count_item:
            position = count_item - 1

        product = await get_one_product({'id': product_items[position]['id']})
        product_id = product.id

        text = f"""
                {product.title}\n{product.description}\n{product.price}руб. x {product_items[position]['count']} = {product.price * product_items[position]['count']}руб.\nтовар {position + 1} из {count_item}
                """

        keyboard = create_cart_menu(product_id, is_first=(position == 0), is_last=(position == count_item - 1),
                                    position=position, kitchen_id=callback_data.kitchen_id)

        media = InputMediaPhoto(media=product.img, caption=text)
        await call.message.edit_media(media=media, reply_markup=keyboard)

@router.callback_query(
    CartCbData.filter(F.action == CartActions.increase)
)
async def increase_count_product_in_cart(call: CallbackQuery, callback_data: CartCbData, state: FSMContext):
    position = callback_data.position
    data = await state.get_data()
    product_items = data.get('product', [])
    product_items[position]['count'] += 1
    await state.update_data(product = product_items)
    count_item = len(product_items)
    product = await get_one_product({'id': product_items[position]['id']})
    product_id = product.id

    text = f"""
            {product.title}\n{product.description}\n{product.price}руб. x {product_items[position]['count']} = {product.price * product_items[position]['count']}руб.\nтовар {position + 1} из {count_item}
            """

    keyboard = create_cart_menu(product_id, is_first=(position == 0), is_last=(position == count_item - 1),position=position, kitchen_id=callback_data.kitchen_id)

    media = InputMediaPhoto(media=product.img, caption=text)
    await call.message.edit_media(media=media, reply_markup=keyboard)

@router.callback_query(
    CartCbData.filter(F.action == CartActions.decrease)
)
async def decrease_count_product_in_cart(call: CallbackQuery, callback_data: CartCbData, state: FSMContext):
    position = callback_data.position
    data = await state.get_data()
    product_items = data.get('product', [])
    if product_items[position]['count'] == 1:
        await delete_product_in_cart(call, callback_data, state)
    else:
        product_items[position]['count'] -= 1
        await state.update_data(product = product_items)
        count_item = len(product_items)
        product = await get_one_product({'id': product_items[position]['id']})
        product_id = product.id

        text = f"""
                {product.title}\n{product.description}\n{product.price}руб. x {product_items[position]['count']} = {product.price * product_items[position]['count']}руб.\nтовар {position + 1} из {count_item}
                """

        keyboard = create_cart_menu(product_id, is_first=(position == 0), is_last=(position == count_item - 1),position=position, kitchen_id=callback_data.kitchen_id)

        media = InputMediaPhoto(media=product.img, caption=text)
        await call.message.edit_media(media=media, reply_markup=keyboard)



@router.callback_query(CartCbData.filter(F.action == CartActions.buy))
async def create_buy(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    data = await state.get_data()
    products = data.get('product', [])
    await state.set_state(Order.product)
    await state.update_data(product = products)
    await state.set_state(Order.payments_type)
    await call.message.answer("Выберите способ оплаты", reply_markup=payment_type_kb())

@router.callback_query(PaymentTypeCb.filter(F.action == PaymentTypeActions.inCash))
async def create_payment_status(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(payment_type = PaymentType.inCash)
    await call.message.answer("Укажите сумму, с которой потребуется сдача, если сдача не нужна, укажите '0' ")
    await state.set_state(Order.change_amount)

@router.callback_query(PaymentTypeCb.filter(F.action == PaymentTypeActions.byCard))
async def create_payment_status(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.update_data(payment_type = PaymentType.byCard)
    await state.set_state(Order.change_amount)
    await state.update_data(change_amount = 0)
    await state.set_state(Order.address)
    await call.message.answer("Укажите адрес доставки")

@router.message(Order.change_amount, IsNumberFilter())
async def create_change_amount(message: types.Message, state: FSMContext):
    await state.update_data(change_amount = int(message.text))
    await state.set_state(Order.address)
    await message.answer("Укажите адрес доставки")

@router.message(Order.change_amount)
async def create_change_amount(message: types.Message):
    await message.answer("Пожалуйста укажите число")

@router.message(Order.address, F.text)
async def order_address_handlers(message: types.Message, state: FSMContext):
    await state.update_data(address=message.text)
    await state.set_state(Order.delivery_time)
    await message.answer("Укажите время доставки в формате '00:00', если хотите указать ближайшее время доставки, просто нажмите на кнопку", reply_markup=time_kb())

@router.message(Order.delivery_time, F.text)
async def create_buy(message: types.Message, state: FSMContext):
    async with session_maker() as session:
        await state.update_data(delivery_time = message.text)
        data = await state.get_data()
        products = data.get('product', [])
        payment_type = data.get('payment_type', PaymentType)
        change_amount = data.get('change_amount', int)
        address = data.get('address', str)
        delivery_time = data.get('delivery_time', str)
        order_id = await create_order(address, payment_type, change_amount, message.from_user.id, delivery_time)
        await state.clear()
        total_price = 0
        text = f"№ заказа: {order_id}\n"
        text += "-" * 30 + "\n"

        for product in products:
            product_item = await get_one_product({'id': product['id']})
            count = product['count']
            product_title = product_item.title
            price_per_item = product_item.price
            price_total = price_per_item * count
            total_price += price_total
            kitchen = await get_kitchen(product_item.owned_id)

            text += f"{product_title} x {count}шт. = {price_total}руб.\n"

            await create_order_assoc(session, order_id, product_item, count)
        await change_order_price(order_id, total_price)
        text += "-" * 30 + "\n"
        text += f"Общая цена заказа: {total_price}руб."

        await message.answer(text, reply_markup=main_kb())
        client = await get_client(message.from_user.id)
        kitchen_answer = f"{text}\n"
        kitchen_answer += "###################\n"
        kitchen_answer += f"Имя: {client.name}\n"
        kitchen_answer += f"Фамилия: {client.lastname}\n"
        kitchen_answer += f"Отчество: {client.patronymic}\n"
        kitchen_answer += f"Номер телефона: {client.number}\n"
        kitchen_answer += "###################\n"
        kitchen_answer += f"Тип оплаты: {payment_type}\n"
        kitchen_answer += f"Сумма, с которой нужна сдача: {change_amount}\n"
        kitchen_answer += f"Адрес доставки: {address}\n"
        kitchen_answer += f"Время доставки: {delivery_time}\n"
        await message.bot.send_message(kitchen.user_id, text=kitchen_answer, reply_markup=create_order_interface(order_id, message.from_user.id))



