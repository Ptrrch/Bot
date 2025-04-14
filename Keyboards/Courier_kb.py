from enum import IntEnum, auto
from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Keyboards.Admin_kb import AdminCbData, AdminActions

class CourierOrderActions(IntEnum):
    inTheWay = auto()
    delivered = auto()


class CourierOrderCb(CallbackData, prefix = "courier_order"):
    action:CourierOrderActions
    order_id: int
    client_id: int


class CourierActions(IntEnum):
    delete = auto()
    update = auto()
    orders = auto()


class CourierItemCbData(CallbackData, prefix="courier_admin"):
    action: CourierActions
    id: int
    name: str


class CourierProfileActions(IntEnum):
    change = auto()



class CourierProfileCb(CallbackData, prefix = "courier_profile"):
    action: CourierProfileActions
    courier_id: int


def courier_change_profile(courier_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Изменить профиль",
            callback_data=CourierProfileCb(
                action=CourierProfileActions.change,
                courier_id=courier_id
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()



def courier_order_in_the_way_interface(order_id: int, client_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Забрал",
            callback_data=CourierOrderCb(
                action=CourierOrderActions.inTheWay,
                order_id=order_id,
                client_id=client_id
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()

def courier_order_delivered_interface(order_id: int, client_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Доставлен",
            callback_data=CourierOrderCb(
                action=CourierOrderActions.delivered,
                order_id=order_id,
                client_id=client_id
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()




def create_courier_interface(courier_id: int, courier_name: str) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Изменить',
            callback_data=CourierItemCbData(
                action=CourierActions.update,
                name=courier_name,
                id=courier_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=CourierItemCbData(
                action=CourierActions.delete,
                name=courier_name,
                id=courier_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=AdminCbData(
                action=AdminActions.couriers,
            ).pack()
        )
    )

    builder.adjust(2)
    return builder.as_markup()


def kitchen_change_keyboard(id: int)-> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=f"delete_kitchen_{id}"
        ),
        InlineKeyboardButton(
            text="Изменить",
            callback_data=f"change_kitchen_{id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=f"get_kitchen"
        )
    )
    return builder.as_markup()


def create_city_for_kitchen_keyboard(data: dict) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in data:
        builder.row(InlineKeyboardButton(
            text=item.title,
            callback_data=f"add_city_for_kitchen_{item.id}"
            )
        )
    builder.adjust(1)
    return builder.as_markup()



def create_city_for_courier_keyboard(data: dict) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in data:
        builder.row(InlineKeyboardButton(
            text=item.title,
            callback_data=f"add_city_for_courier_{item.id}"
            )
        )
    builder.adjust(1)
    return builder.as_markup()



def create_city_for_client_keyboard(data: dict) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in data:
        builder.row(InlineKeyboardButton(
            text=item.title,
            callback_data=f"add_city_for_client_{item.id}"
            )
        )
    builder.adjust(1)
    return builder.as_markup()