
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_city_keyboard(data: dict) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if data is not None:
        for item in data:
            builder.row(InlineKeyboardButton(
                text=item.title,
                callback_data=f"get_city_item_{item.id}"
                )
            )
    builder.row(
        InlineKeyboardButton(
            text='➕ Добавить город',
            callback_data='create_new_city'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='🔄 Обновить',
            callback_data='refresh_city'
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


def city_change_keyboard(id: int)-> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=f"delete_city_{id}"
        ),
        InlineKeyboardButton(
            text="Изменить",
            callback_data=f"change_city_{id}"
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=f"get_city"
        )
    )
    return builder.as_markup()