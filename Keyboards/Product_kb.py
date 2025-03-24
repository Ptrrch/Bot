from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_product_keyboard(data: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in data:
        builder.row(InlineKeyboardButton(
            text=item.title,
            callback_data=f"get_product_item_{item.id}"
            )
        )
    builder.row(
        InlineKeyboardButton(
            text='➕ Добавить позицию',
            callback_data='create_new_product'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='🔄 Обновить',
            callback_data='refresh_product'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='👋 Назад',
            callback_data='back_home'
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def product_change_keyboard(id: int)-> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=f"delete_product_{id}"
        ),
        InlineKeyboardButton(
            text="Изменить",
            callback_data=f"change_product_{id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=f"get_product"
        )
    )
    return builder.as_markup()