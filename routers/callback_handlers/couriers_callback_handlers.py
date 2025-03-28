from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from Keyboards.Admin_kb import AdminCourierCbData, AdminCourierActions, get_couriers_for_admin_keyboards
from Keyboards.Courier_kb import create_courier_interface, CourierItemCbData, CourierActions
from database.crud.couriers_crud import get_courier, delete_courier, get_couriers

router = Router(name=__name__)

@router.callback_query(
    AdminCourierCbData.filter(F.action == AdminCourierActions.details)
)
async def show_info_courier(call: CallbackQuery, callback_data: AdminCourierCbData):
    courier = await get_courier(callback_data.user_id)
    text = markdown.text(
        markdown.hbold(f"{courier.name}\n"),
            markdown.hbold(f"{courier.lastname}\n"),
            markdown.hbold(courier.number)

    )
    await call.message.edit_text(text, reply_markup=create_courier_interface(callback_data.user_id, callback_data.name))

@router.callback_query(
    CourierItemCbData.filter(F.action == CourierActions.delete)
)
async def delete_courier_handlers(call: CallbackQuery, callback_data: AdminCourierCbData):
    await delete_courier(callback_data.id)
    couriers = await get_couriers()
    keyboard = get_couriers_for_admin_keyboards(couriers)
    await call.message.edit_text(
        text="Список курьеров:",
        reply_markup=keyboard,
    )
#
#
# @router.callback_query(
#     ClientCbData.filter(F.action == ClientActions.delete)
# )
# async def delete_client_handlers(call: CallbackQuery, callback_data: ClientCbData):
#     await delete_client(callback_data.id)
#     await call.answer()
#     clients = await get_clients()
#     keyboard = get_client_for_admin_keyboards(clients)
#     await call.message.edit_text(
#         text="Список клиентов:",
#         reply_markup=keyboard,
#     )