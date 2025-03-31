from enum import IntEnum, auto
from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import markdown
from aiogram.utils.keyboard import InlineKeyboardBuilder


class MenyFirstActions(IntEnum):
    show = auto()
    back = auto()

class MenuFirstCbData(CallbackData, prefix="menu_first"):
    action: MenyFirstActions
    kitchen_id: int
    kitchen_title: str

class MenySecondActions(IntEnum):
    show = auto()
    back = auto()

class MenuSecondCbData(CallbackData, prefix="menu_second"):
    action: MenyFirstActions
    product_id: int
    kitchen_id: int


class MenyThirdActions(IntEnum):
    append = auto()
    back = auto()

class MenuThirdCbData(CallbackData, prefix="menu_third"):
    action: MenyThirdActions
    product_id: int


class CartActions(IntEnum):
    append = auto()
    next = auto()
    last = auto()
    back = auto()


class CartCbData(CallbackData, prefix = "menu_second"):
    action: CartActions
    position: int
    kitchen_id: int
    id: int


def create_kitchen_menu(data: list) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if data is not None:
        for item in data:
            builder.row(
                InlineKeyboardButton(
                    text=item.title,
                    callback_data=MenuFirstCbData(
                        action=MenyFirstActions.show,
                        kitchen_id=item.id,
                        kitchen_title=item.title
                    ).pack()
                )
            )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=MenuFirstCbData(
                action=MenyFirstActions.back,
                kitchen_id=0,
                kitchen_title=""
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def create_cart_menu(product_id: int, is_first: False, is_last: False, position: int, kitchen_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Добавить",
            callback_data=CartCbData(
                action=CartActions.append,
                id = product_id,
                position=position,
                kitchen_id=kitchen_id
            ).pack()
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data=CartCbData(
                action=CartActions.back,
                id=product_id,
                position=position,
                kitchen_id=kitchen_id
            ).pack()
        )
    )

    if not is_first:
        builder.row(
            InlineKeyboardButton(
                text="Предыдущий",
                callback_data=CartCbData(
                    action=CartActions.last,
                    id=product_id,
                    position=position,
                    kitchen_id=kitchen_id
                ).pack()
            )
        )
    if not is_last:
        builder.row(
            InlineKeyboardButton(
                text="Следующий",
                callback_data=CartCbData(
                    action=CartActions.next,
                    id=product_id,
                    position=position,
                    kitchen_id=kitchen_id
                ).pack()
            )
        )
    builder.adjust(2)
    return builder.as_markup()


def create_product_menu(data: list, kitchen_id: int) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if data is not None:
        for item in data:
            builder.row(
                InlineKeyboardButton(
                    text=item.title,
                    callback_data=MenuSecondCbData(
                        action=MenySecondActions.show,
                        product_id=item.id,
                        kitchen_id=kitchen_id
                    ).pack()
                )
            )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=MenuSecondCbData(
                action=MenySecondActions.back,
                product_id=0,
                kitchen_id=0
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def create_product_interface(product_id: int) ->InlineKeyboardMarkup:
    builder  = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Добавить",
            callback_data=MenuThirdCbData(
                action=MenyThirdActions.append,
                product_id=product_id
            ).pack()
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data=MenuThirdCbData(
                action=MenyThirdActions.back,
                product_id=product_id
            ).pack()
        ),
    )
    builder.adjust(2)
    return builder.as_markup()


def title_decoration(title: str):
    text = markdown.text(
        markdown.hitalic(title)
    )
    return text