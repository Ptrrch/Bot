from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


class AdminActions(IntEnum):
    cities = auto()
    kitchens = auto()
    couriers = auto()
    clients = auto()
    orders = auto()


class AdminCbData(CallbackData, prefix="admins"):
    action: AdminActions


class AdminClientActions(IntEnum):
    details = auto()


class AdminClientCbData(CallbackData, prefix="admins_client"):
    action: AdminClientActions
    user_id: int
    name: str
    lastname: str


def create_admin_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Города',
            callback_data=AdminCbData(action=AdminActions.cities).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Заведения',
            callback_data=AdminCbData(action=AdminActions.kitchens).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Курьеры',
            callback_data=AdminCbData(action=AdminActions.couriers).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Клиенты',
            callback_data=AdminCbData(action=AdminActions.clients).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Заказы',
            callback_data=AdminCbData(action=AdminActions.orders).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()




from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_client_for_admin_keyboards(data: list):
    builder = InlineKeyboardBuilder()

    # Проверяем, что data является списком и не пустой
    if isinstance(data, list) and data:
        for item in data:
            builder.row(
                InlineKeyboardButton(
                    text=f'{item.name}',
                    callback_data=AdminClientCbData(
                        action=AdminClientActions.details,
                        user_id=item.id,
                        name=item.name,
                        lastname=item.lastname
                    ).pack()
                )
            )

    builder.row(
        InlineKeyboardButton(
            text="Добавить клиента",
            callback_data="add_city"  # Укажите подходящий callback_data
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data="go_back"  # Укажите подходящий callback_data
        )
    )

    return builder.as_markup()




