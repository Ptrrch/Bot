from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from Keyboards.Admin_kb import AdminClientCbData, AdminClientActions, get_client_for_admin_keyboards
from Keyboards.Client_kb import create_client_interface, ClientCbData, ClientActions, create_client_orders_keyboards, \
    ClientOrdersCb, ClientOrderActions, back_client_orders_keyboards, ClientOrdersBackCb, ClientOrderBackActions
from database.crud.clients_crud import get_client, delete_client, get_clients
from database.crud.kitchens_crud import get_kitchen
from database.crud.orders_crud import get_order, get_orders, get_order_assoc, get_orders_assoc
from database.crud.product_crud import get_one_product
from database.engine import session_maker
from filters.isClient import ClientFilter

router = Router(name=__name__)
router.message.filter(ClientFilter())

@router.message(F.text == '📖 Мои заказы', ClientFilter())
async def show_kitchen_list(message: types.Message) -> None:
    client_item = await get_client(message.from_user.id)
    data = await get_orders(client_item.user_id)
    if not data:
        await message.answer("Кажется у вас еще нет заказов")
    else:
        await message.answer("Вот ваши заказы:", reply_markup=create_client_orders_keyboards(data))


@router.callback_query(ClientOrdersCb.filter(F.action == ClientOrderActions.back))
async def back_client_interface(call: CallbackQuery):
    await call.answer()
    await call.message.delete()


@router.callback_query(ClientOrdersCb.filter(F.action == ClientOrderActions.show))
async def show_item_in_client_orders(call: CallbackQuery, callback_data: ClientOrdersCb):
    await call.answer()
    kitchen_id = 0
    order = await get_order(callback_data.order_id)
    text = f"""Номер заказа: {order.id}\n"""
    text += f"-----------------------\n"
    text += f"Общая стоимость заказа: {order.order_price}\n"
    text += f"-----------------------\n"
    async with session_maker() as session:
        products = await get_order_assoc(session, callback_data.order_id)
        for item in products.products_details:
            product = await get_one_product({'id': item.product_id})
            text += f"{product.title}: {product.price} x {item.count} = {product.price*item.count}руб.\n"
            kitchen_id = product.owned_id
    await call.message.answer(text, reply_markup=back_client_orders_keyboards())
    text += f"-----------------------\n"
    kitchen = await get_kitchen(kitchen_id)
    text += f"Наименование заведения: {kitchen.title}\n"


@router.callback_query(ClientOrdersBackCb.filter(F.action == ClientOrderBackActions.back))
async def back_show_item(call: CallbackQuery):
    await call.answer()
    await call.message.delete()




@router.callback_query(
    AdminClientCbData.filter(F.action == AdminClientActions.details)
)
async def show_info_client(call: CallbackQuery, callback_data: AdminClientCbData):
    client = await get_client(callback_data.user_id)
    text = markdown.text(
        markdown.hbold(client.name),
        markdown.text(
            markdown.hbold(client.lastname),

        ),
        markdown.text(
            markdown.hbold(client.number)
        )
    )
    await call.message.edit_text(text, reply_markup=create_client_interface(callback_data.user_id, callback_data.name, callback_data.lastname))


@router.callback_query(
    ClientCbData.filter(F.action == ClientActions.delete)
)
async def delete_client_handlers(call: CallbackQuery, callback_data: ClientCbData):
    await delete_client(callback_data.id)
    await call.answer()
    clients = await get_clients()
    keyboard = get_client_for_admin_keyboards(clients)
    await call.message.edit_text(
        text="Список клиентов:",
        reply_markup=keyboard,
    )

