
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_kitchen_keyboard(data: dict) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for item in data:
        builder.row(InlineKeyboardButton(
            text=item.title,
            callback_data=f"get_kitchen_item_{item.id}"
            )
        )
    builder.row(
        InlineKeyboardButton(
            text='➕ Добавить Кухню',
            callback_data='create_new_kitchen'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='🔄 Обновить',
            callback_data='refresh_kitchen'
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
