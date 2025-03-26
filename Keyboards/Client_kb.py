from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder






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