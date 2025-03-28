from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Keyboards.Admin_kb import AdminClientCbData, AdminClientActions, AdminActions, AdminCbData


class ClientActions(IntEnum):
    delete = auto()
    update = auto()
    orders = auto()
    back = auto()



class ClientCbData(CallbackData, prefix="client_details"):
    action: ClientActions
    id: int
    name: str


def create_client_interface(id:int, name:str, lastname: str):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Заказы",
            callback_data=ClientCbData(
                action=ClientActions.orders,
                id=id,
                name=name
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=ClientCbData(
                action=ClientActions.delete,
                id=id,
                name=name
            ).pack()
        ),
        InlineKeyboardButton(
            text="Изменить",
            callback_data=ClientCbData(
                action=ClientActions.update,
                id=id,
                name=name
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=AdminCbData(
                action=AdminActions.clients,
            ).pack()
        )
    )


    return builder.as_markup()



def create_kitchen_for_client_keyboard(data: dict) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in data:
        builder.row(InlineKeyboardButton(
            text=item.title,
            callback_data=f"get_kitchen_for_client_item_{item.id}"
            )
        )

    builder.adjust(1)
    return builder.as_markup()


def create_product_from_kitchen_keyboard(data: dict) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in data:
        builder.row(InlineKeyboardButton(
            text=item.title,
            callback_data=f"get_item_from_kitchen_{item.id}"
            )
        )
    builder.row(InlineKeyboardButton(
        text="Назад",
        callback_data="get_kitchen_list"
    )
    )
    builder.adjust(1)
    return builder.as_markup()

def interface_from_item(id: int) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(
        text="Назад",
        callback_data=f"get_kitchen_for_client_item_{id}"
    )
    )
    builder.adjust(1)
    return builder.as_markup()