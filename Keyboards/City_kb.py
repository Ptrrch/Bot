from enum import IntEnum, auto

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Keyboards.Admin_kb import AdminCbData, AdminActions


class CitiesActions(IntEnum):
    delete = auto()
    update = auto()


class CitiesItemCbData(CallbackData, prefix="cities"):
    action: CitiesActions
    id: int
    title: str


def create_cities_keyboard(city_id: int, city_title: str) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Изменить',
            callback_data=CitiesItemCbData(
                action=CitiesActions.update,
                id = city_id,
                title=city_title

            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=CitiesItemCbData(
                action=CitiesActions.delete,
                id=city_id,
                title=city_title
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=AdminCbData(
                action=AdminActions.cities,
            ).pack()
        )
    )

    builder.adjust(2)
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