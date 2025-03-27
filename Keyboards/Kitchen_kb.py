from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Keyboards.Admin_kb import AdminCbData, AdminActions


class KitchenActions(IntEnum):
    delete = auto()
    update = auto()
    product = auto()


class KitchenItemCbData(CallbackData, prefix="kitchen"):
    action: KitchenActions
    id: int
    title: str



def create_kitchen_keyboard(kitchen_id: int, kitchen_title: str) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Изменить',
            callback_data=KitchenItemCbData(
                action=KitchenActions.update,
                title=kitchen_title,
                id=kitchen_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=KitchenItemCbData(
                action=KitchenActions.delete,
                title=kitchen_title,
                id=kitchen_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=AdminCbData(
                action=AdminActions.kitchens,
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
