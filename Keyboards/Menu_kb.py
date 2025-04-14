from enum import IntEnum, auto
from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils import markdown
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from database.models import Product, PaymentType


class MenyFirstActions(IntEnum):
    show = auto()
    back = auto()

class MenuFirstCbData(CallbackData, prefix="menu_first"):
    action: MenyFirstActions
    kitchen_id: int
    kitchen_title: str

class MenuSecondActions(IntEnum):
    show = auto()
    cart =auto()
    back = auto()

class MenuSecondCbData(CallbackData, prefix="menu_second"):
    action: MenuSecondActions
    product_id: int
    kitchen_id: int


class MenuThirdActions(IntEnum):
    append = auto()
    back = auto()

class MenuThirdCbData(CallbackData, prefix="menu_third"):
    action: MenuThirdActions
    product_id: int


class CartActions(IntEnum):
    increase = auto()
    decrease = auto()
    next = auto()
    last = auto()
    delete = auto()
    back = auto()
    buy = auto()


class CartCbData(CallbackData, prefix = "cart"):
    action: CartActions
    position: int
    kitchen_id: int
    id: int


class PaymentTypeActions(IntEnum):
    inCash = auto()
    byCard = auto()



class PaymentTypeCb(CallbackData, prefix = "callback_data"):
    action: PaymentTypeActions


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


def create_cart_menu(
        product_id: int,
        is_first: False,
        is_last: False,
        position: int,
        kitchen_id: int,
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="-1",
            callback_data=CartCbData(
                action=CartActions.decrease,
                id=product_id,
                position=position,
                kitchen_id=kitchen_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="+1",
            callback_data=CartCbData(
                action=CartActions.increase,
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
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=CartCbData(
                action=CartActions.delete,
                id=product_id,
                position=position,
                kitchen_id=kitchen_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Оформить заказ",
            callback_data=CartCbData(
                action=CartActions.buy,
                id=product_id,
                position=position,
                kitchen_id=kitchen_id
            ).pack()
        )
    )
    builder.row(
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
                        action=MenuSecondActions.show,
                        product_id=item.id,
                        kitchen_id=kitchen_id
                    ).pack()
                )
            )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=MenuSecondCbData(
                action=MenuSecondActions.back,
                product_id=0,
                kitchen_id=0
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Корзина",
            callback_data=MenuSecondCbData(
                action=MenuSecondActions.cart,
                product_id=0,
                kitchen_id=kitchen_id
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
                action=MenuThirdActions.append,
                product_id=product_id
            ).pack()
        ),
        InlineKeyboardButton(
            text="Назад",
            callback_data=MenuThirdCbData(
                action=MenuThirdActions.back,
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





def payment_type_kb():
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=PaymentType.inCash,
            callback_data= PaymentTypeCb(
                action= PaymentTypeActions.inCash
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text=PaymentType.byCard,
            callback_data=PaymentTypeCb(
                action=PaymentTypeActions.byCard
            ).pack()
        )
    )
    builder.adjust(2)
    return builder.as_markup()