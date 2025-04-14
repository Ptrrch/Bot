import random
from idlelib.undo import Command
from pyexpat.errors import messages

from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from Keyboards.Admin_kb import AdminKitchensCbData, AdminKitchensActions, get_kitchens_for_admin_keyboards
from Keyboards.Base_kb import time_kb, kitchen_kb
from Keyboards.Courier_kb import courier_order_in_the_way_interface
from Keyboards.Kitchen_kb import create_kitchen_keyboard, KitchenItemCbData, KitchenActions, KitchenOrderCb, \
    KitchenOrderActions, move_kitchen_keyboard, KitchenMoveCb, KitchenMoveActions, create_product_for_kitchen_keyboard, \
    KitchenMenuCb, KitchenMenuActions, product_change_kitchen_keyboard, KitchenMenuItemCb, KitchenMenuItemActions, \
    create_change_menu, ChangeCbData, ChangeActions, create_order_interface, create_preparing_state_order_keyboard, \
    StateOrderKitchenCb, StateOrderKitchenActions, create_courier_inform_state_order_keyboard
from Keyboards.Menu_kb import PaymentTypeCb, PaymentTypeActions, payment_type_kb
from Keyboards.Product_kb import create_product_keyboard
from database.crud.cities_crud import get_one_city
from database.crud.clients_crud import get_client
from database.crud.couriers_crud import get_couriers_from_city, increment_courier_counter
from database.crud.kitchens_crud import delete_kitchen, get_kitchens, get_kitchen, get_kitchen_with_user_id
from database.crud.orders_crud import change_state_order, get_order_assoc, create_order_assoc, get_order, \
    delete_order_product_assoc, change_order_address, change_order_payment_type, change_order_change_amount, \
    change_order_price, append_courier_for_order, change_order_delivery_time
from database.crud.product_crud import get_products, get_one_product, delete_product
from database.engine import session_maker
from database.models import StateOrder, PaymentType
from filters.isKitchen import KitchenFilter
from filters.isNumber import IsNumberFilter
from routers.callback_handlers.kitchens_callback_handlers.states import Change, ChangeOrder

router = Router(name=__name__)
router.message.filter(KitchenFilter())

@router.message(F.text == '📚 Кухня', KitchenFilter())
async def show_kitchen_interface(message: types.Message):
    title ="-"
    kitchen = await get_kitchen_with_user_id(message.from_user.id)
    city = await get_one_city(kitchen.city_id)
    if city:
        title = city.title
    text = f"""Название: {kitchen.title}\nОписание: {kitchen.description}\nАдрес: {title}, {kitchen.address}\nНомер: {kitchen.number}
    """
    await message.answer(text, reply_markup=move_kitchen_keyboard(kitchen.id))


@router.callback_query(KitchenMoveCb.filter(F.action == KitchenMoveActions.menu))
async def show_menu_interface(call: CallbackQuery, callback_data:KitchenMoveCb):
    await call.answer()
    products = await get_products({'owned_id': callback_data.kitchen_id})
    await call.message.edit_text(text="Меню", reply_markup=create_product_for_kitchen_keyboard(callback_data.kitchen_id, products))


@router.callback_query(KitchenMenuCb.filter(F.action == KitchenMenuActions.back))
async def back_on_kitchen(call: CallbackQuery, callback_data:KitchenMenuCb):
    await call.answer()
    kitchen = await get_kitchen(callback_data.kitchen_id)
    title = "-"
    city = await get_one_city(kitchen.city_id)
    if city:
        title = city.title
    text = f"""Название: {kitchen.title}\nОписание: {kitchen.description}\nАдрес: {title}, {kitchen.address}\nНомер: {kitchen.number}
        """
    await call.message.edit_text(text, reply_markup=move_kitchen_keyboard(kitchen.id))


@router.callback_query(KitchenMenuCb.filter(F.action == KitchenMenuActions.details))
async def show_product_details(call: CallbackQuery, callback_data: KitchenMenuCb):
    await call.message.delete()
    product = await get_one_product({'id': callback_data.product_id})


    text = f"{product.title}\n{product.description}\nЦена: {product.price}.р"

    await call.message.answer_photo(
        photo=product.img,
        caption=text,
        reply_markup=product_change_kitchen_keyboard(callback_data.product_id, callback_data.kitchen_id)
    )

@router.callback_query(KitchenMenuItemCb.filter(F.action == KitchenMenuItemActions.delete))
async def delete_product_in_menu(call: CallbackQuery, callback_data: KitchenMenuItemCb):
    await delete_product({'id': callback_data.product_id})
    products = await get_products({'owned_id': callback_data.kitchen_id})
    await call.message.delete()
    await call.message.answer(text="Меню",
                                 reply_markup=create_product_for_kitchen_keyboard(callback_data.kitchen_id, products))

@router.callback_query(KitchenMenuItemCb.filter(F.action == KitchenMenuItemActions.back))
async def back_to_kitchen_menu(call: CallbackQuery, callback_data: KitchenMenuItemCb):
    await call.message.delete()
    products = await get_products({'owned_id': callback_data.kitchen_id})
    await call.message.answer(text="Меню",
                                 reply_markup=create_product_for_kitchen_keyboard(callback_data.kitchen_id, products))

@router.callback_query(AdminKitchensCbData.filter(F.action == AdminKitchensActions.details))
async def create_kitchen_details(call:CallbackQuery, callback_data: AdminKitchensCbData):
    text = markdown.text(
        markdown.hbold(f"{callback_data.title}")
    )
    await call.message.edit_text(text=text, reply_markup=create_kitchen_keyboard(callback_data.id, callback_data.title))

@router.callback_query(KitchenItemCbData.filter(F.action == KitchenActions.delete))
async def delete_kitchen_handlers(call: CallbackQuery, callback_data: KitchenItemCbData):
    await delete_kitchen(callback_data.id)
    kitchens = await get_kitchens()
    keyboard = get_kitchens_for_admin_keyboards(kitchens)
    await call.message.edit_text(
        text="Список Заведений:",
        reply_markup=keyboard,
    )

@router.callback_query(KitchenItemCbData.filter(F.action == KitchenActions.product))
async def product_from_kitchen_handlers(call: CallbackQuery, callback_data: KitchenItemCbData):
    products = await get_products({'owned_id': callback_data.id})
    keyboard = create_product_keyboard(callback_data.id, callback_data.title, products)
    text = markdown.text(
        markdown.hbold(f"{callback_data.title}")
    )
    await call.message.edit_text(
        text=text,
        reply_markup=keyboard,
    )

@router.callback_query(KitchenOrderCb.filter(F.action == KitchenOrderActions.reject))
async def product_from_kitchen_handlers(call: CallbackQuery, callback_data: KitchenOrderCb):
    await call.answer()
    await change_state_order(callback_data.order_id, StateOrder.cancelled)
    await call.message.bot.send_message(callback_data.client_id, text="Ваш заказ отменен")
    await call.message.delete()


def get_random_id_with_min_counter(data):
    if not data:
        return None

    min_counter = min(item['counter'] for item in data)

    min_ids = [item['id'] for item in data if item['counter'] == min_counter]

    return random.choice(min_ids)


@router.callback_query(KitchenOrderCb.filter(F.action == KitchenOrderActions.accept))
async def product_from_kitchen_handlers(call: CallbackQuery, callback_data: KitchenOrderCb):
    await change_state_order(callback_data.order_id, StateOrder.inTheReview)
    await call.message.bot.send_message(callback_data.client_id, text="Ваш заказ принят")
    kitchen = await get_kitchen_with_user_id(call.from_user.id)
    couriers = await get_couriers_from_city(kitchen.city_id)
    courier_list = []
    for item in couriers:
        courier_list.append({'id': item.user_id, 'counter': item.order_counter})
    courier_id = get_random_id_with_min_counter(courier_list)
    await append_courier_for_order(callback_data.order_id, courier_id)
    await increment_courier_counter(courier_id)

    await call.message.edit_reply_markup(reply_markup=create_preparing_state_order_keyboard(callback_data.order_id, callback_data.client_id))


@router.callback_query(StateOrderKitchenCb.filter(F.action == StateOrderKitchenActions.preparing))
async def state_preparing_handlers(call: CallbackQuery, callback_data:StateOrderKitchenCb):
    await call.answer()
    await change_state_order(callback_data.order_id, StateOrder.prepared)
    await call.message.edit_reply_markup(reply_markup=create_courier_inform_state_order_keyboard(callback_data.order_id, callback_data.client_id))
    await call.message.bot.send_message(callback_data.client_id, "Ваш заказ начали готовить")


@router.callback_query(StateOrderKitchenCb.filter(F.action == StateOrderKitchenActions.courierInform))
async def state_preparing_handlers(call: CallbackQuery, callback_data:StateOrderKitchenCb):
    await call.answer()
    await change_state_order(callback_data.order_id, StateOrder.courierInform)
    order = await get_order(callback_data.order_id)
    text = await create_courier_text(callback_data.order_id, callback_data.client_id)
    await call.message.bot.send_message(order.courier_id, text, reply_markup=courier_order_in_the_way_interface(callback_data.order_id, callback_data.client_id))
    await call.message.delete_reply_markup()



@router.callback_query(KitchenOrderCb.filter(F.action == KitchenOrderActions.changeAddress))
async def change_order_address_handlers(call: CallbackQuery, callback_data:KitchenOrderCb, state: FSMContext):
    await call.message.answer("Укажите адрес доставки")
    await state.set_state(ChangeOrder.order_id)
    await state.update_data(order_id = callback_data.order_id)
    await state.set_state(ChangeOrder.address)


@router.message(ChangeOrder.address)
async def change_order_address_handles_state(message: types.Message, state: FSMContext):
    data = await state.update_data(address = message.text)
    await change_order_address(data['address'], data['order_id'])
    order = await get_order(data['order_id'])
    await message.bot.send_message(order.client_id,
                                   f"Адрес изменен на {data['address']} ")
    await state.clear()


@router.callback_query(KitchenOrderCb.filter(F.action == KitchenOrderActions.changeTime))
async def change_order_address_handlers(call: CallbackQuery, callback_data:KitchenOrderCb, state: FSMContext):
    await call.message.answer("Укажите время доставки в формате '00:00', если хотите указать ближайшее время доставки, просто нажмите на кнопку", reply_markup=time_kb())
    await state.set_state(ChangeOrder.order_id)
    await state.update_data(order_id = callback_data.order_id)
    await state.set_state(ChangeOrder.delivery_time)

@router.message(ChangeOrder.delivery_time)
async def change_order_address_handles_state(message: types.Message, state: FSMContext):
    data = await state.update_data(delivery_time = message.text)
    await change_order_delivery_time(data['delivery_time'], data['order_id'])
    order = await get_order(data['order_id'])
    await message.bot.send_message(order.client_id,
                                   f"Время изменено на {data['delivery_time']} ")
    await state.clear()
    await message.answer("Вы изменили время", reply_markup=kitchen_kb())



@router.callback_query(KitchenOrderCb.filter(F.action == KitchenOrderActions.changeType))
async def change_order_type_handlers(call: CallbackQuery, callback_data:KitchenOrderCb, state: FSMContext):
    await call.message.answer("Укажите тип оплаты", reply_markup=payment_type_kb())
    await state.set_state(ChangeOrder.order_id)
    await state.update_data(order_id = callback_data.order_id)
    await state.set_state(ChangeOrder.payments_type)



@router.callback_query(ChangeOrder.payments_type, PaymentTypeCb.filter(F.action == PaymentTypeActions.byCard))
async def change_order_address_handles_state(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    data = await state.update_data(payment_type = PaymentType.byCard)
    await change_order_payment_type(data['payment_type'], data['order_id'])
    order = await get_order(data['order_id'])
    await call.message.bot.send_message(order.client_id, f"Тип оплаты изменен на {data['payment_type']}")
    await state.clear()


@router.callback_query(ChangeOrder.payments_type, PaymentTypeCb.filter(F.action == PaymentTypeActions.inCash))
async def change_order_address_handles_state(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    data = await state.update_data(payment_type = PaymentType.inCash)
    await change_order_payment_type(data['payment_type'], data['order_id'])
    order = await get_order(data['order_id'])
    await call.message.bot.send_message(order.client_id, f"Тип оплаты изменен на {data['payment_type']}")
    await state.clear()


@router.callback_query(KitchenOrderCb.filter(F.action == KitchenOrderActions.changeAmount))
async def change_order_amount_handlers(call: CallbackQuery, callback_data:KitchenOrderCb, state: FSMContext):
    await call.answer("Укажите сумму, с которой понадобится сдача")
    await state.set_state(ChangeOrder.order_id)
    await state.update_data(order_id = callback_data.order_id)
    await state.set_state(ChangeOrder.change_amount)

@router.message(ChangeOrder.change_amount, IsNumberFilter())
async def create_change_amount(message: types.Message, state: FSMContext):
    data = await state.update_data(change_amount = int(message.text))
    await change_order_change_amount(data['change_amount'], data['order_id'])
    order = await get_order(data['order_id'])
    await message.bot.send_message(order.client_id, f"Сумма, с которой понадобится сдача изменена на {data['change_amount']} ")
    await state.clear()


@router.message(ChangeOrder.change_amount)
async def create_change_amount(message: types.Message):
    await message.answer("Пожалуйста укажите число")




@router.callback_query(KitchenOrderCb.filter(F.action == KitchenOrderActions.change))
async def product_from_kitchen_handlers(call: CallbackQuery, callback_data: KitchenOrderCb, state: FSMContext):
    await call.answer()
    await state.set_state(Change.product)
    products = []
    async with session_maker() as session:
        data = await get_order_assoc(session, callback_data.order_id)
        for item in data.products_details:
            product = {"id": item.product_id, "count": item.count}
            products.append(product)
        await state.update_data(product = products)
        data = await state.get_data()
        product_items = data.get('product', [])
        if len(product_items) == 0:
            await call.answer("Ваша корзина пуста")
        else:
            await call.answer()
            is_first = False
            is_last = False

            product = await get_one_product({"id": product_items[0]['id']})
            kitchen_id = product.owned_id
            count_item = len(product_items)
            if count_item == 1:
                is_last = True
                is_first = True
            if count_item > 1:
                is_first = True
            text = f"""
                    {product.title}\n{product.description}\n{product.price}руб. x {product_items[0]['count']} = {product.price * product_items[0]['count']}руб.\nтовар {1} из {count_item}
                    """
            keyboard = create_change_menu(product.id, is_first, is_last, position=0, kitchen_id=kitchen_id, order_id=callback_data.order_id)
        await call.message.answer(text = text, reply_markup=keyboard)


@router.callback_query(
    ChangeCbData.filter(F.action == ChangeActions.back),
)
async def delete_product_menu_keyboards(call: CallbackQuery):
    await call.message.delete()

@router.callback_query(
    ChangeCbData.filter(F.action == ChangeActions.next),
)

async def move_next_product_menu_keyboards(call: CallbackQuery, callback_data:ChangeCbData, state: FSMContext):
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
    keyboard = create_change_menu(product_id, False, is_last, position=position, kitchen_id=callback_data.kitchen_id, order_id=callback_data.order_id)

    await call.message.edit_text(text = text, reply_markup=keyboard)


@router.callback_query(
    ChangeCbData.filter(F.action == ChangeActions.last),
)
async def move_last_product_menu_keyboards(call: CallbackQuery, callback_data: ChangeCbData, state: FSMContext):
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
    keyboard = create_change_menu(product_id, is_first, False, position=position,kitchen_id=callback_data.kitchen_id, order_id=callback_data.order_id)

    await call.message.edit_text(text = text, reply_markup=keyboard)


@router.callback_query(
    ChangeCbData.filter(F.action == ChangeActions.delete),
)
async def delete_product_in_cart(call: CallbackQuery, callback_data: ChangeCbData, state: FSMContext):
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

        keyboard = create_change_menu(product_id, is_first=(position == 0), is_last=(position == count_item - 1),
                                    position=position, kitchen_id=callback_data.kitchen_id, order_id=callback_data.order_id)

        await call.message.edit_text(text=text, reply_markup=keyboard)

@router.callback_query(
    ChangeCbData.filter(F.action == ChangeActions.increase)
)
async def increase_count_product_in_cart(call: CallbackQuery, callback_data: ChangeCbData, state: FSMContext):
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

    keyboard = create_change_menu(product_id, is_first=(position == 0), is_last=(position == count_item - 1),position=position, kitchen_id=callback_data.kitchen_id, order_id=callback_data.order_id)


    await call.message.edit_text(text = text, reply_markup=keyboard)

@router.callback_query(
    ChangeCbData.filter(F.action == ChangeActions.decrease)
)
async def decrease_count_product_in_cart(call: CallbackQuery, callback_data: ChangeCbData, state: FSMContext):
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

        keyboard = create_change_menu(product_id, is_first=(position == 0), is_last=(position == count_item - 1),position=position, kitchen_id=callback_data.kitchen_id, order_id=callback_data.order_id)

        await call.message.edit_text(text = text, reply_markup=keyboard)


@router.callback_query(
    ChangeCbData.filter(F.action == ChangeActions.change)
)
async def commit_change(call: CallbackQuery, callback_data: ChangeCbData,  state: FSMContext):
    await call.message.delete()
    async with session_maker() as session:
        await delete_order_product_assoc(callback_data.order_id)
        data = await state.get_data()
        products = data.get('product', [])
        await state.clear()
        total_price = 0
        text = f"№ заказа: {callback_data.order_id}\n"
        text += "-" * 30 + "\n"

        for product in products:
            product_item = await get_one_product({'id': product['id']})
            count = product['count']
            product_title = product_item.title
            price_per_item = product_item.price
            price_total = price_per_item * count
            total_price += price_total

            text += f"{product_title} x {count}шт. = {price_total}руб.\n"

            await create_order_assoc(session, callback_data.order_id, product_item, count)
        await change_order_price(callback_data.order_id, total_price)
        text += "-" * 30 + "\n"
        text += f"Общая цена заказа: {total_price}руб."


        order = await get_order(callback_data.order_id)
        client = await get_client(order.client_id)
        order_text = f"{text}\n"
        order_text += "###################\n"
        order_text += f"Имя: {client.name}\n"
        order_text += f"Фамилия: {client.lastname}\n"
        order_text += f"Отчество: {client.patronymic}\n"
        order_text += f"Номер телефона: {client.number}\n"
        order_text += "###################\n"
        order_text += f"Время доставки: {order.delivery_time}\n"
        order_text += f"Тип оплаты: {order.payment_type}\n"
        order_text += f"Сумма, с которой нужна сдача: {order.change_amount}\n"
        order_text += f"Адрес доставки: {order.address}\n"
        await call.message.answer(text, reply_markup=create_order_interface(callback_data.order_id, client.user_id))
        kitchen_answer = f"Ваш заказ изменен:\n{text}\n"

        await call.message.bot.send_message(client.user_id, text=kitchen_answer)


async def create_courier_text(order_id: int, client_id: int):
    async with session_maker() as session:
        product_list = ""
        kitchen = 0
        order = await get_order_assoc(session, order_id)
        for item in order.products_details:
            product = await get_one_product({'id': item.product_id})
            kitchen = await get_kitchen(product.owned_id)
            product_list += f"{product.title}: x {item.count} = {product.price*item.count}руб.\n"
        text = f"""Номер заказа: {order.id}\nЗаведение:\n {kitchen.title}\n{kitchen.address}\n{kitchen.number}\n-----------------------\n
        """
        text += product_list
        text += "-----------------------\nЗаказчик:\n"
        client = await get_client(client_id)
        text +=f"{client.name} {client.lastname} {client.patronymic}\n{client.number}\n{order.address}\n"
        text += "-----------------------\nДанные по заказу: \n"
        text += f"Тип: {order.payment_type}\nК оплате: {order.order_price}руб.\nСдача нужна с {order.change_amount}руб."
        return text








