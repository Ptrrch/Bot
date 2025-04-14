from datetime import datetime
from enum import IntEnum, auto
from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Keyboards.Admin_kb import  AdminActions, AdminCbData


class ClientActions(IntEnum):
    delete = auto()
    update = auto()
    orders = auto()
    back = auto()



class ClientCbData(CallbackData, prefix="client_details"):
    action: ClientActions
    id: int
    name: str


class ClientOrderActions(IntEnum):
    show = auto()
    back = auto()


class ClientOrdersCb(CallbackData, prefix="client_orders"):
    action: ClientOrderActions
    order_id: int

class ClientOrderBackActions(IntEnum):
    back = auto()


class ClientOrdersBackCb(CallbackData, prefix="client_orders_back"):
    action: ClientOrderBackActions
    order_id: int


def convert_datetime_format(date_input):
    if not isinstance(date_input, datetime):
        raise TypeError("Input must be a datetime object")
    return date_input.strftime('%d:%m:%Y')


def create_client_orders_keyboards(data: dict):
    builder = InlineKeyboardBuilder()
    for item in data:
        builder.row(
            InlineKeyboardButton(
                text=convert_datetime_format(item.created),
                callback_data=ClientOrdersCb(
                    action=ClientOrderActions.show,
                    order_id=item.id
                ).pack()
            )
        )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=ClientOrdersCb(
                action=ClientOrderActions.back,
                order_id=0
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()

def back_client_orders_keyboards():
    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=ClientOrdersBackCb(
                action=ClientOrderBackActions.back,
                order_id=0
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()

def create_client_interface(id:int, name:str, lastname: str):
    builder = InlineKeyboardBuilder()
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