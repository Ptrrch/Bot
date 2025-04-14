from enum import IntEnum, auto
from sys import prefix

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from Keyboards.Admin_kb import AdminCbData, AdminActions


class KitchenActions(IntEnum):
    delete = auto()
    update = auto()
    product = auto()


class KitchenItemCbData(CallbackData, prefix="kitchen_admin"):
    action: KitchenActions
    id: int
    title: str


class KitchenOrderActions(IntEnum):
    reject = auto()
    change = auto()
    changeAddress = auto()
    changeType = auto()
    changeAmount = auto()
    changeTime = auto()
    accept = auto()

class KitchenOrderCb(CallbackData, prefix = "kitchen_menu"):
    action: KitchenOrderActions
    order_id: int
    client_id: int


class KitchenMoveActions(IntEnum):
    menu = auto()
    profile = auto()


class KitchenMoveCb(CallbackData, prefix="kitchen_move"):
    action: KitchenMoveActions
    kitchen_id: int


class KitchenMenuActions(IntEnum):
    details = auto()
    append = auto()
    back = auto()


class KitchenMenuCb(CallbackData, prefix="kitchen_menu_interface"):
    action: KitchenMenuActions
    product_id: int
    kitchen_id: int

class KitchenMenuItemActions(IntEnum):
    delete = auto()
    change = auto()
    back = auto()


class KitchenMenuItemCb(CallbackData, prefix="kitchen_item_menu"):
    action: KitchenMenuItemActions
    product_id: int
    kitchen_id: int


class ChangeActions(IntEnum):
    increase = auto()
    decrease = auto()
    next = auto()
    last = auto()
    delete = auto()
    back = auto()
    change = auto()


class ChangeCbData(CallbackData, prefix = "cart_change"):
    action: ChangeActions
    position: int
    order_id: int
    kitchen_id: int
    id: int


class StateOrderKitchenActions(IntEnum):
    preparing = auto()
    courierInform = auto()



class StateOrderKitchenCb(CallbackData, prefix = "state_order_kitchen"):
    action: StateOrderKitchenActions
    order_id: int
    client_id: int

def create_preparing_state_order_keyboard(order_id: int, client_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Начали готовить",
            callback_data=StateOrderKitchenCb(
                action=StateOrderKitchenActions.preparing,
                order_id=order_id,
                client_id=client_id
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()



def create_courier_inform_state_order_keyboard(order_id: int, client_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Сообщить курьеру",
            callback_data=StateOrderKitchenCb(
                action=StateOrderKitchenActions.courierInform,
                order_id=order_id,
                client_id=client_id
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()



def create_order_interface(order_id: int, client_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Принять",
            callback_data=KitchenOrderCb(
                action=KitchenOrderActions.accept,
                order_id=order_id,
                client_id=client_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Изменить содержание заказа",
            callback_data=KitchenOrderCb(
                action=KitchenOrderActions.change,
                order_id=order_id,
                client_id = client_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Изменить адрес доставки",
            callback_data=KitchenOrderCb(
                action=KitchenOrderActions.changeAddress,
                order_id=order_id,
                client_id=client_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Изменить тип оплаты",
            callback_data=KitchenOrderCb(
                action=KitchenOrderActions.changeType,
                order_id=order_id,
                client_id=client_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Изменить сумму для сдачи",
            callback_data=KitchenOrderCb(
                action=KitchenOrderActions.changeAmount,
                order_id=order_id,
                client_id=client_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Изменить время доставки",
            callback_data=KitchenOrderCb(
                action=KitchenOrderActions.changeTime,
                order_id=order_id,
                client_id=client_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Отклонить",
            callback_data=KitchenOrderCb(
                action=KitchenOrderActions.reject,
                order_id=order_id,
                client_id = client_id
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def create_kitchen_keyboard(kitchen_id: int, kitchen_title: str) ->InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Изменить',
            callback_data=KitchenItemCbData(
                action=KitchenActions.update,
                title=kitchen_title,
                id=kitchen_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=KitchenItemCbData(
                action=KitchenActions.delete,
                title=kitchen_title,
                id=kitchen_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Продукты",
            callback_data=KitchenItemCbData(
                action=KitchenActions.product,
                title=kitchen_title,
                id=kitchen_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=AdminCbData(
                action=AdminActions.kitchens,
            ).pack()
        )
    )

    builder.adjust(2)
    return builder.as_markup()


def move_kitchen_keyboard(kitchen_id: int):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Меню",
            callback_data=KitchenMoveCb(
                action=KitchenMoveActions.menu,
                kitchen_id=kitchen_id
            ).pack()
        ),
        InlineKeyboardButton(
            text="Изменить профиль",
            callback_data=KitchenMoveCb(
                action=KitchenMoveActions.profile,
                kitchen_id=kitchen_id
            ).pack()
        )
    )
    builder.adjust(2)
    return builder.as_markup()


def create_product_for_kitchen_keyboard(kitchen_id:int, data: dict) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if data is not None:
        for item in data:
            builder.row(InlineKeyboardButton(
                text=item.title,
                callback_data=KitchenMenuCb(
                    action=KitchenMenuActions.details,
                    kitchen_id=kitchen_id,
                    product_id=item.id
                ).pack()
            )
        )
    builder.row(
        InlineKeyboardButton(
            text='➕ Добавить позицию',
            callback_data=KitchenMenuCb(
                action=KitchenMenuActions.append,
                kitchen_id=kitchen_id,
                product_id=0
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='👋 Назад',
            callback_data=KitchenMenuCb(
                action=KitchenMenuActions.back,
                kitchen_id=kitchen_id,
                product_id=0
            ).pack()
        )
    )
    builder.adjust(1)
    return builder.as_markup()


def product_change_kitchen_keyboard(product_id: int, kitchen_id: int)-> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=KitchenMenuItemCb(
                action=KitchenMenuItemActions.delete,
                product_id=product_id,
                kitchen_id=kitchen_id
            ).pack()
        ),
        InlineKeyboardButton(
            text="Изменить",
            callback_data=KitchenMenuItemCb(
                action=KitchenMenuItemActions.change,
                product_id=product_id,
                kitchen_id=kitchen_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=KitchenMenuItemCb(
                action=KitchenMenuItemActions.back,
                product_id=product_id,
                kitchen_id=kitchen_id
            ).pack()
        )
    )
    builder.adjust(2)
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


def create_change_menu(
        product_id: int,
        is_first: False,
        is_last: False,
        position: int,
        kitchen_id: int,
        order_id: int
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="-1",
            callback_data=ChangeCbData(
                action=ChangeActions.decrease,
                id=product_id,
                position=position,
                kitchen_id=kitchen_id,
                order_id = order_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="+1",
            callback_data=ChangeCbData(
                action=ChangeActions.increase,
                id=product_id,
                position=position,
                kitchen_id=kitchen_id,
                order_id=order_id
            ).pack()
        )
    )
    if not is_first:
        builder.row(
            InlineKeyboardButton(
                text="Предыдущий",
                callback_data=ChangeCbData(
                    action=ChangeActions.last,
                    id=product_id,
                    position=position,
                    kitchen_id=kitchen_id,
                    order_id=order_id
                ).pack()
            )
        )
    if not is_last:
        builder.row(
            InlineKeyboardButton(
                text="Следующий",
                callback_data=ChangeCbData(
                    action=ChangeActions.next,
                    id=product_id,
                    position=position,
                    kitchen_id=kitchen_id,
                    order_id=order_id
                ).pack()
            )
        )
    builder.row(
        InlineKeyboardButton(
            text="Удалить",
            callback_data=ChangeCbData(
                action=ChangeActions.delete,
                id=product_id,
                position=position,
                kitchen_id=kitchen_id,
                order_id=order_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Отправить изменения",
            callback_data=ChangeCbData(
                action=ChangeActions.change,
                id=product_id,
                position=position,
                kitchen_id=kitchen_id,
                order_id=order_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text="Назад",
            callback_data=ChangeCbData(
                action=ChangeActions.back,
                id=product_id,
                position=position,
                kitchen_id=kitchen_id,
                order_id=order_id
            ).pack()
        )
    )
    builder.adjust(2)
    return builder.as_markup()