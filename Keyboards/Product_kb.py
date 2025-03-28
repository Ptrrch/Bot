from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Keyboards.Admin_kb import AdminKitchensActions, AdminKitchensCbData
from database.crud.product_crud import get_products


class ProductActions(IntEnum):
    details = auto()
    create = auto()
    delete = auto()
    update = auto()
    back = auto()


class ProductCbData(CallbackData, prefix="product_from_kitchens"):
    action: ProductActions
    id: int
    title: str

def create_product_keyboard(kitchen_id:int, kitchen_title:str, data: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if data is not None:
        for item in data:
            builder.row(InlineKeyboardButton(
                text=item.title,
                callback_data=ProductCbData(
                    action=ProductActions.details,
                    id = item.id,
                    title=item.title
                ).pack()
                )
            )
    builder.row(
        InlineKeyboardButton(
            text='➕ Добавить позицию',
            callback_data=ProductCbData(
                action=ProductActions.create,
                id=kitchen_id,
                title=kitchen_title
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='👋 Назад',
            callback_data=AdminKitchensCbData(
                action=AdminKitchensActions.details,
                id=kitchen_id,
                title=kitchen_title
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def product_change_keyboard(id: int)-> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=ProductCbData(
                action=ProductActions.delete,
                id=id,
                title=""
            ).pack()
        ),
        InlineKeyboardButton(
            text="Изменить",
            callback_data=ProductCbData(
                action=ProductActions.update,
                id=id,
                title=""
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=ProductCbData(
                action=ProductActions.back,
                id=0,
                title=""
            ).pack()
        )
    )
    return builder.as_markup()


def create_kitchen_for_product_keyboard(data: dict) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in data:
        builder.row(InlineKeyboardButton(
            text=item.title,
            callback_data=f"add_kitchen_for_product_{item.id}"
            )
        )
    builder.adjust(1)
    return builder.as_markup()
