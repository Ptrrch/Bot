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
    back = auto()


class AdminCbData(CallbackData, prefix="admins"):
    action: AdminActions


class AdminClientActions(IntEnum):
    details = auto()
    create = auto()


class AdminClientCbData(CallbackData, prefix="admins_client"):
    action: AdminClientActions
    user_id: int
    name: str
    lastname: str


class AdminCourierActions(IntEnum):
    details = auto()
    create = auto()


class AdminCourierCbData(CallbackData, prefix="admins_courier"):
    action: AdminCourierActions
    user_id: int
    name: str


class AdminCitiesActions(IntEnum):
    details = auto()
    create = auto()

class AdminCitiesCbData(CallbackData, prefix="admins_cities"):
    action: AdminCitiesActions
    id: int
    title: str



class AdminKitchensActions(IntEnum):
    details = auto()
    create = auto()


class AdminKitchensCbData(CallbackData, prefix="admins_kitchens"):
    action: AdminKitchensActions
    id: int
    title: str

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
    builder.adjust(1)
    return builder.as_markup()


def get_client_for_admin_keyboards(data: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()



    for item in data:
        builder.row(
            InlineKeyboardButton(
                text=f'{item.name}',
                callback_data=AdminClientCbData(
                    action=AdminClientActions.details,
                    user_id=item.user_id,
                    name=item.name,
                    lastname=item.lastname
                ).pack()
            )
        )

    builder.row(
        InlineKeyboardButton(
            text="Добавить клиента",
            callback_data=AdminClientCbData(
                action=AdminClientActions.create,
                user_id=0,
                name="",
                lastname=""
            ).pack()
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data=AdminCbData(
                action=AdminActions.back,
            ).pack()
        )
    )

    return builder.as_markup()


def get_couriers_for_admin_keyboards(data: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if data is not None:
        for item in data:
            builder.row(
                InlineKeyboardButton(
                    text=f'{item.name}',
                    callback_data=AdminCourierCbData(
                        action=AdminCourierActions.details,
                        user_id=item.user_id,
                        name=item.name,
                    ).pack()
                )
            )

    builder.row(
        InlineKeyboardButton(
            text="Добавить курьера",
            callback_data=AdminCourierCbData(
                action=AdminCourierActions.create,
                user_id=0,
                name=""
                ).pack()
            ),
        InlineKeyboardButton(
            text="Назад",
            callback_data=AdminCbData(
                action=AdminActions.back,
            ).pack()
        )
    )

    return builder.as_markup()


def get_cities_for_admin_keyboards(data: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()


    for item in data:
        builder.row(
            InlineKeyboardButton(
                text=f'{item.title}',
                callback_data=AdminCitiesCbData(
                    action=AdminCitiesActions.details,
                    id = item.id,
                    title= item.title
                ).pack()
            )
        )

    builder.row(
        InlineKeyboardButton(
            text="Добавить Город",
            callback_data=AdminCitiesCbData(
                action=AdminCitiesActions.create,
                id = 0,
                title=""
            ).pack()
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data=AdminCbData(
                action=AdminActions.back,
            ).pack()
        )
    )

    return builder.as_markup()


def get_kitchens_for_admin_keyboards(data: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()


    for item in data:
        builder.row(
            InlineKeyboardButton(
                text=f'{item.title}',
                callback_data=AdminKitchensCbData(
                    action=AdminKitchensActions.details,
                    id = item.id,
                    title= item.title
                ).pack()
            )
        )

    builder.row(
        InlineKeyboardButton(
            text="Добавить Кухню",
            callback_data=AdminKitchensCbData(
                action=AdminKitchensActions.create,
                id=0,
                title=""
            ).pack()
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data=AdminCbData(
                action=AdminActions.back,
            ).pack()
        )
    )

    return builder.as_markup()



