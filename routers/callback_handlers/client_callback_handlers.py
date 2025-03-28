from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils import markdown

from Keyboards.Admin_kb import AdminClientCbData, AdminClientActions, get_client_for_admin_keyboards
from Keyboards.Client_kb import create_client_interface, ClientCbData, ClientActions
from database.crud.clients_crud import get_client, delete_client, get_clients

router = Router(name=__name__)

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