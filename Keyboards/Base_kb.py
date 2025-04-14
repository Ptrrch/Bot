from enum import IntEnum, auto

from aiogram import types
from aiogram.filters.callback_data import CallbackData
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def main_kb():
    kb_list = [
        [KeyboardButton(text="📚 Каталог заведений")],
        [KeyboardButton(text="📖 Мои заказы")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def kitchen_kb():
    kb_list = [
        [KeyboardButton(text="📚 Кухня")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard



def courier_kb():
    kb_list = [
        [KeyboardButton(text="📚 Курьер")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def admin_kb():
    kb_list = [
        [KeyboardButton(text="📚 Каталог заведений")],
        [KeyboardButton(text="Панель админа 🔧")]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard

def contact_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(
        types.KeyboardButton(text="Отправить контакт", request_contact=True)
    )

    return builder.as_markup(resize_keyboard=True)

def time_kb():
    kb_list = [
        [KeyboardButton(text="Ближайшее")],
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=kb_list,
        resize_keyboard=True,
        one_time_keyboard=False,
        input_field_placeholder="Воспользуйтесь меню:"
    )
    return keyboard


class ClientProfileActions(IntEnum):
    create = auto()
    update = auto()


class ClientProfileCb(CallbackData, prefix='client_profile'):
    action: ClientProfileActions
    id: int


class UserFormActions(IntEnum):
    agree = auto()
    disagree = auto()

class UserFormCb(CallbackData, prefix = "user_form"):
    action: UserFormActions
    id:int


def agree_with_form_kb(id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Не согласен",
            callback_data=UserFormCb(
                action=UserFormActions.disagree,
                id = id
            ).pack()
        ),
        InlineKeyboardButton(
            text="Согласен",
            callback_data=UserFormCb(
                action=UserFormActions.agree,
                id = id
            ).pack()
        )
    )
    builder.adjust(2)
    return builder.as_markup()

def client_profile_kb(user_id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Создать",
            callback_data=ClientProfileCb(
                action=ClientProfileActions.create,
                id = user_id
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()